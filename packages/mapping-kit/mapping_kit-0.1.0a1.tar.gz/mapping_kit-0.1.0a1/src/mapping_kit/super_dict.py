# https://docs.python.org/3/library/stdtypes.html#mapping-types-dict
from collections import OrderedDict
from collections.abc import Mapping
from typing import (Any, Callable, Hashable, Iterable, MutableMapping,
                    Self, TypeAlias)


_SuperDictInit: TypeAlias = Mapping | Iterable[tuple[Hashable, Any]]


class SuperDict(MutableMapping, dict):
    """A super ``dict``-like object that has ``collections.defaultdict``,
    ``collections.OrderedDict``, case-insensitiviy and recursion rolled
    into one.

    Initially sourced from requests.structures and heavily modified.
    Implements all methods and operations of
    ``MutableMapping`` as well as dict's ``copy``. When key case-insensitivity
    is turned on, also provides various dict methods with newer ``_origcase``
    versions.

    All keys are expected to be strings. The structure remembers the
    case of the last key to be set, and ``iter(instance)``,
    ``keys()``, ``items()``, ``iterkeys()``, and ``iteritems()``
    will contain case-sensitive keys. However, querying and contains
    testing is case-insensitive::

        cid = SuperDict()
        cid['Accept'] = 'application/json'
        cid['aCCEPT'] == 'application/json'  # True
        list(cid) == ['Accept']  # True

    For example, ``headers['content-encoding']`` will return the
    value of a ``'Content-Encoding'`` response header, regardless
    of how the header name was originally stored.

    If the constructor, ``.update``, or equality comparison
    operations are given keys that have equal ``.lower()``s, the
    behavior is undefined.
    """
    def __init__(self,
                 data: _SuperDictInit = {},
                 *,
                 parent: Self | None = None,
                 key_ignorecase: bool = False,
                 ordereddict: bool = False,
                 default_factory: Callable[[], Any] | None = None,
                 recursive: bool = False,
                 **kwargs):
        self.parent = parent
        self._key_ignorecase = key_ignorecase
        self._ordereddict = ordereddict
        self.default_factory = default_factory
        self._recursive = recursive

        self._store = OrderedDict() if self._ordereddict else dict()
        self.update(dict(data, **kwargs))  # calls __setitem__

    def __contains__(self, item):
        return ((_str_lower(item) if self._key_ignorecase else item)
                in self._store)

    # def __cmp__(self, other):
    #     __le__, __lt__, __ge__, __gt__
    #     raise AttributeError("")

    def __delitem__(self, key):
        if self._key_ignorecase:
            key = _str_lower(key)
        del self._store[key]

    def __eq__(self, other):
        return (isinstance(other, self.__class__)
                and self._store == other._store
                and self.parent == other.parent
                and self.key_ignorecase == other.key_ignorecase)

    def __getitem__(self, key):
        if key in self._store:
            gotitem = self._store[_str_lower(key)][1] if self._key_ignorecase \
                else self._store[key]
        else:
            if self._default_factory is not None:
                gotitem = self.__missing__(key)
            else:
                raise KeyError(key)
        return gotitem

    def __iter__(self):
        return self._store.__iter__()

    def __len__(self):
        return len(self._store)

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        if key not in self._store:
            self[key] = self._default_factory()
        return self[key]

    def __or__(self, other):
        self_ignorecase_flipped = False
        if self.key_ignorecase:
            self.key_ignorecase = False
            self_ignorecase_flipped = True

        other_ignorecase_flipped = False
        if isinstance(other, self.__class__):
            if other.key_ignorecase:
                other.key_ignorecase = False
                other_ignorecase_flipped = True

        orred = self._store | other

        if self_ignorecase_flipped:
            self.key_ignorecase = True

        if other_ignorecase_flipped:
            other.key_ignorecase = True

        return other.like(orred) if isinstance(other, self.__class__) \
            else orred

    def __repr__(self):
        return (f"{self.__class__.__name__}({dict(self.items_keys_origcase())},"
                f" parent={self.parent},"
                f" key_ignorecase={self._key_ignorecase},"
                f" ordereddict={self._ordereddict},"
                f" default_factory={self._default_factory},"
                f" recursive={self._recursive})")

    def __setitem__(self, key, value):
        if self._recursive and isinstance(value, Mapping):
            value = self.like(value)

        if self._key_ignorecase:
            # Use the lowercased key for lookups, but store the actual
            # key alongside the value
            self._store[_str_lower(key)] = (key, value)
        else:
            self._store[key] = value

    @property
    def default_factory(self):
        return self._default_factory

    @default_factory.setter
    def default_factory(self, factory: Callable[[], Any]):
        if not (factory is None or isinstance(factory, Callable)):
            raise TypeError(f"'{type(factory)}' object is not callable")
        self._default_factory = factory

    @property
    def key_ignorecase(self):
        return self._key_ignorecase

    @key_ignorecase.setter
    def key_ignorecase(self, ignorecase: bool):
        if not (ignorecase := bool(ignorecase)) == self._key_ignorecase:
            self._key_ignorecase = ignorecase
            if self._key_ignorecase:
                self._store = {_str_lower(key): (key, value)
                               for key, value in self._store.items()}
            else:
                self._store = {value[0]: value[1]
                               for value in self._store.values()}

    @property
    def store(self):
        return self._store

    def __to_origcase(self):
        pass

    def clear(self):
        self._store.clear()
        self.parent = None

    def copy(self):
        return self.like(
            self._store.values() if self._key_ignorecase else dict(self)
        )

    def get(self, key, default=None):
        return self._store.get(key, default)

    def get_origcase(self, key, default=None):
        if self._key_ignorecase:
            got = default
            if (key_lower := _str_lower(key)) in self._store:
                value = self._store[key_lower]
                if value[0] == key:
                    got = value[1]
        else:
            got = self._store.get(key, default)
        return got

    def items(self):
        return ((key_lower, value[1])
                for key_lower, value in self._store.items()) \
            if self._key_ignorecase else self._store.items()

    def items_keys_origcase(self):
        return self._store.values() if self._key_ignorecase \
            else self._store.items()

    def keys(self):
        return self._store.keys()

    def keys_origcase(self):
        return (value[0] for value in self._store.values()) \
            if self._key_ignorecase else self._store.keys()

    def pop(self, key, default):
        return self._store.pop(key, default)

    def pop_origcase(self, key, default):
        if self._key_ignorecase:
            popped = default
            if (key_lower := _str_lower(key)) in self._store:
                value = self._store[key_lower]
                if value[0] == key:
                    popped = value[1]
                self._store.pop(key_lower)
        else:
            popped = self._store.pop(key, default)
        return popped

    def popitem(self):
        popped_item = self._store.popitem()
        if self._key_ignorecase:
            key_lower, value = popped_item
            popped_item = (key_lower, value[1])
        return popped_item

    def popitem_origcase(self):
        popped_item = self._store.popitem()
        if self._key_ignorecase:
            popped_item = popped_item[1]
        return popped_item

    def setdefault(self, key, default=None):
        if self._key_ignorecase:
            set_value = self._store.setdefault(
                _str_lower(key), (key, default)
            )[1]
        else:
            set_value = self._store.setdefault(key, default)
        return set_value

    # def update(self, *args, **kwargs):
    #     self._store.update(*args, **kwargs)

    def values(self):
        return (value[1] for value in self._store.values()) \
            if self._key_ignorecase else self._store.values()

    def like(self, data: _SuperDictInit) -> Self:
        return self.__class__(data,
                              parent=self.parent,
                              key_ignorecase=self._key_ignorecase,
                              recursive=self._recursive,
                              ordereddict=self._ordereddict,
                              default_factory=self._default_factory)


def _str_lower(text: Any) -> Any:
    return text.lower() if isinstance(text, str) else text
