from collections import OrderedDict
from .str import to_var_format, to_var_format_classname


class TypeBase:
    _typed_cls_suffix = None
    _typed_name = None

    def __init__(self, manager):
        self.manager = manager

    @classmethod
    def get_typed_name(cls):
        if cls._typed_name:
            return cls._typed_name
        return cls.__name__[:-len(cls._typed_cls_suffix)]

    @classmethod
    def on_typed_registered(cls, types):
        pass

    @classmethod
    def is_my_typed(cls, obj):
        if isinstance(obj, type):
            return issubclass(obj, cls)
        else:
            return cls.is_my_typed(obj.__class__)


class TypesBase:
    def __init__(self):
        self._maps = OrderedDict()

    def __getitem__(self, item):
        return self._maps[item]

    def keys(self):
        return self._maps.keys()

    def values(self):
        return self._maps.values()

    def items(self):
        return self._maps.items()

    def get(self, typed, default=None):
        return self._maps.get(typed, default)

    def register(self, cls):
        self._maps[cls.get_typed_name()] = cls
        cls.on_typed_registered(self)
        return cls

    @staticmethod
    def to_label(s):
        return '-'.join(to_var_format(s))

    @staticmethod
    def to_classname(s):
        return to_var_format_classname(to_var_format(s))

    @staticmethod
    def to_pairs(s):
        array = to_var_format(s)
        return '-'.join(array), to_var_format_classname(array)


class ManagerBase:
    types: TypesBase = None
