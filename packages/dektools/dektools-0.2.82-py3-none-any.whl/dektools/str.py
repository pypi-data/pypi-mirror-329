import re
import string
import codecs
import unicodedata
import random
import hashlib
from collections.abc import Mapping


def is_wide_char(c):
    return "\u2E80" <= c <= "\u9FFF"


class Unicode:
    def __init__(self, s):
        self.value = s

    def __len__(self):
        result = 0
        for c in self.value:
            if is_wide_char(c):
                result += 1
            result += 1
        return result

    def __getitem__(self, item):
        if isinstance(item, int):
            start = item
            stop = item + 1
            step = 1
        else:
            start = item.start or 0
            stop = len(self.value) if item.stop is None else item.stop
            if stop < 0:
                stop = len(self.value) + stop
            step = item.step or 1
        result = ''
        cursor = 0
        for c in self.value:
            if cursor >= stop:
                break
            elif cursor >= start:
                result += c
            if is_wide_char(c):
                cursor += 1
            cursor += step
        return result


class FormatDict(Mapping):
    empty = type('empty', (), {})

    def __init__(self, kwargs, missing=None):
        self.kwargs = kwargs
        self.missing = missing

    @staticmethod
    def __missing(key):
        return f'{{{key}}}'

    def __getitem__(self, item):
        value = self.kwargs.get(item, self.empty)
        if value is self.empty:
            return (self.missing or self.__missing)(item)
        else:
            return value

    def __iter__(self):
        return iter(self.kwargs)

    def __len__(self):
        return len(self.kwargs)


formatter = string.Formatter()


def str_format_partial(s, kwargs, missing=None):
    return formatter.vformat(s, (), FormatDict(kwargs, missing))


def str_escaped(s):
    return codecs.getdecoder("unicode_escape")(s.encode('utf-8'))[0]


def str_split(s, sep):
    for x in s.split(sep):
        x = x.strip()
        if x:
            yield x


def str_custom_escaped_split(s, delim, escaped='\\'):
    ret = []
    current = []
    itr = iter(s)
    for ch in itr:
        if ch == escaped:
            try:
                # skip the next character; it has been escaped!
                current.append(escaped)
                current.append(next(itr))
            except StopIteration:
                pass
        elif ch == delim:
            # split! (add current to the list and reset it)
            ret.append(''.join(current))
            current = []
        else:
            current.append(ch)
    ret.append(''.join(current))
    return ret


def str_custom_escaped(s, mapping=None, escaped='\\'):
    mapping = {} if mapping is None else mapping
    r = ""
    cursor = 0
    length = len(s)
    while cursor < length:
        c = s[cursor]
        if c == escaped:
            cursor += 1
            c = s[cursor]
            r += mapping.get(c, c)
        else:
            r += c
        cursor += 1
    return r


def str_align_number(index, total):
    lt = len(str(total))
    li = len(str(index))
    return max(0, lt - li) * '0' + str(index)


_var_marker_ld = set(string.ascii_lowercase + string.digits)
_var_marker_u = set(string.ascii_uppercase)
_var_marker_d = set(string.digits)


def to_var_format(*str_list):
    r = []
    for x in str_list:
        s = ""
        for i in range(len(x)):
            if x[i] in _var_marker_ld:
                s += x[i]
            else:
                if s:
                    r.append(s)
                    s = ""
                if x[i] in _var_marker_u:
                    s += x[i].lower()
        if s:
            r.append(s)
    if r and r[0][0] in _var_marker_d:
        r[0] = '_' + r[0]
    return r


def to_var_format_classname(r):
    return ''.join(x.capitalize() for i, x in enumerate(r))


def to_var_format_camel(r):
    return ''.join(x if i == 0 else x.capitalize() for i, x in enumerate(r))


def to_var_format_pascal(r):
    return ''.join(x.capitalize() for x in r)


def to_var_format_hungarian(r):
    return '_'.join(r)


def to_var_format_py(r):
    return ''.join(r)


def str_special_escape(s, escape='\\'):
    r = ""
    escaping = False
    for x in s:
        if not escaping and x == escape:
            escaping = True
        else:
            r += x
            escaping = False
    return r


def str_format_var(s, begin='{', end='}', escape='\\'):
    fmt = ['']
    args = []
    arg = None
    escaping = False
    same = begin == end
    swap = False
    for x in s:
        if not escaping and x == escape:
            escaping = True
        else:
            if escaping:
                if arg is None:
                    fmt[-1] += x
                else:
                    arg += x
            else:
                if x == begin and (not same or not swap):
                    swap = True
                    if arg is None:
                        arg = ""
                    else:
                        arg += x
                else:
                    if x == end:
                        swap = False
                        if arg is None:
                            fmt[-1] += x
                        else:
                            args.append(arg)
                            arg = None
                            fmt.append('')
                    else:
                        if arg is None:
                            fmt[-1] += x
                        else:
                            arg += x
            escaping = False
    return lambda xx, ma=None, mi=None: _str_format_var_final(fmt, xx, ma, mi), args


def _str_format_var_final(fmt, args, mapping=None, missing=None):
    s = ""
    cursor = 0
    while True:
        s += fmt[cursor]
        if cursor == len(fmt) - 1:
            break
        arg = args[cursor]
        if mapping and arg in mapping:
            arg = mapping[arg]
        elif missing:
            arg = missing(arg)
        s += str(arg)
        cursor += 1
    return s


def decimal_to_short_str(num, sequence):
    lst = []
    sequence_length = len(sequence)
    num = num - 1
    if num > sequence_length - 1:
        while True:
            d = int(num / sequence_length)
            remainder = num % sequence_length
            if d <= sequence_length - 1:
                lst.insert(0, sequence[remainder])
                lst.insert(0, sequence[d - 1])
                break
            else:
                lst.insert(0, sequence[remainder])
                num = d - 1
    else:
        lst.append(sequence[num])
    return "".join(lst)


def tab_str(s, n, p=4, sl=False):  # s: list of str or str
    if isinstance(s, str):
        s = [s]
    r = []
    for x in s:
        if sl:
            x = x.strip()
            if x:
                r.append(x)
        else:
            r.append(x)
    r = '\n'.join(r).split('\n')
    return '\n'.join([' ' * n * p + x for x in r])


def startswith(s, *items, reverse=False):
    for item in items:
        if reverse:
            yield item.startswith(s)
        else:
            yield s.startswith(item)


def endswith(s, *items, reverse=False):
    for item in items:
        if reverse:
            yield item.endswith(s)
        else:
            yield s.endswith(item)


def slugify(value, allow_unicode=False, sep='', case=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    if case is True:
        value = value.upper()
    elif case is False:
        value = value.lower()
    value = re.sub(r'[^\w\s-]', sep, value.lower())
    return re.sub(rf'[{sep}\s]+', sep, value).strip(f'-_{sep}')


def shorted(s, limit, count, offset=-1):
    if len(s) <= limit:
        return s
    count = min(limit, count)
    length = len(s) - limit + count
    if count % 2:
        hl = count // 2 + 1
        end = -1
    else:
        hl = count // 2
        end = None
    replaced = hashlib.shake_256(s.encode('utf-8')).hexdigest(hl)
    if end is not None:
        replaced = replaced[:end]
    if offset >= 0:
        offset = min(offset, limit - len(replaced))
        return s[:offset] + replaced + s[offset + length:]
    else:
        offset = max(offset, len(replaced) - limit - 1)
        return s[:offset + 1 - length] + replaced + ("" if offset == -1 else s[offset + 1:])


def triple_find(s: str | bytes, first, left, right):
    i = s.find(first)
    if i == -1:
        return None
    il = s.rfind(left, 0, i)
    if il == -1:
        return None
    ir = s.find(right, i + len(first))
    if ir == -1:
        return None
    return s[il + len(left):ir]


def replace(s, d):
    return re.sub("|".join(d), lambda x: d[x.group(0)], s)


def hex_random(length):
    ss = string.digits + 'abcdef'
    return ''.join(random.choice(ss) for _ in range(length))


class Fragment:
    @classmethod
    def format(cls, content, amap):
        if not amap:
            return content
        fragment = cls(content, *amap)
        from_list = iter(amap.keys())
        to_list = iter(amap.values())
        result = fragment[0]
        for i in range(1, len(fragment)):
            f, t = next(from_list), next(to_list)
            if i < len(fragment) - 1:
                x = fragment.content[fragment.indexes[i - 1] + len(f):fragment.indexes[i]]
            else:
                x = fragment.content[fragment.indexes[i - 1] + len(f):]
            result += t + x
        return result

    @classmethod
    def replace(cls, content, list_of_pairs, reverse=False):
        if not list_of_pairs:
            return content
        indexes = [1, 0] if reverse else [0, 1]
        fragment = cls(content, *(pairs[indexes[0]] for pairs in list_of_pairs), sep=True)
        result = ''
        for i, pairs in enumerate(list_of_pairs):
            result += fragment[2 * i] + pairs[indexes[1]]
        tail = fragment[2 * len(list_of_pairs):]
        if tail:
            result += tail
        return result

    @classmethod
    def replace_safe_again(cls, content, list_of_pairs, reverse=False):
        # For each pair, do not contain each other
        try:
            content = cls.replace(content, list_of_pairs, reverse)
        except IndexError as e:
            try:
                cls(content, *(pairs[0 if reverse else 1] for pairs in list_of_pairs))
            except IndexError:
                raise e
        else:
            return content

    def __init__(self, content: str | bytes, *separators, sep=False):
        self.content = content
        indexes = self.split(content, separators)
        if sep:
            self.indexes = [indexes[i // 2] + len(separators[i // 2]) if i % 2 else indexes[i // 2]
                            for i in range(2 * len(separators))]
        else:
            self.indexes = indexes

    def __len__(self):
        return len(self.indexes) + 1

    def __getitem__(self, item):
        ii = list(range(len(self.indexes) + 1))[item]
        if not isinstance(ii, list):
            ii = [ii]
        result = self.type()
        for i in ii:
            if i == 0:
                result += self.content[:self.indexes[i]]
            elif i == len(self.indexes):
                result += self.content[self.indexes[i - 1]:]
            else:
                result += self.content[self.indexes[i - 1]:self.indexes[i]]
        return result

    def sub(self, begin: tuple | int, end: tuple | int | None = None):
        if isinstance(begin, int):
            index, offset = 0, begin
        else:
            index, offset = begin
        _begin = self.indexes[index] + offset
        if isinstance(end, int):  # length
            _end = _begin + end
        elif isinstance(end, tuple):  # to index
            index, offset = end
            _end = self.indexes[index] + offset
        else:  # to end
            _end = None
        return self.content[_begin:_end]

    @property
    def type(self):
        return self.content.__class__

    @staticmethod
    def split(content, separators):
        indexes = []
        cursor = 0
        for separator in separators:
            index = content.find(separator, cursor)
            if index == -1:
                raise IndexError(f"Cannot find {separator} from {cursor}")
            indexes.append(index)
            cursor = index + len(separator)
        return indexes


if __name__ == '__main__':
    fx, a = str_format_var('aaa{bbb}ccc{ddd}')
    print(fx([x.upper() for x in a]))

    fx, a = str_format_var('aaa$bbb$ccc$ddd$', '$', '$')
    print(fx([x.upper() for x in a]))

    import hashlib

    print(decimal_to_short_str(
        int(hashlib.md5('test'.encode("ascii")).hexdigest(), 16),
        string.digits + string.ascii_letters + '_')
    )

    print(replace("I have a dog but not a cat.", {"dog": "cat", "cat": "dog"}))

    print(Fragment(string.ascii_uppercase.encode(), b'EF', b'OP', b'UV')[::2])
    print(Fragment(string.ascii_uppercase.encode(), b'EF', b'OP', b'UV', sep=True)[::2])

    print(Fragment.format(string.ascii_uppercase, {'EF': 'ef', 'OP': 'op', 'UV': 'uv'}))

    print(triple_find(string.ascii_uppercase.encode(), b'OP', b'EF', b'UV'))
