from abc import abstractmethod
from typing import Any


class YAMLPathComponent:
    """A sequence of PathComponents identifies an element in a YAML file.
    
    Elements can be the keys in a mapping, a value in a mapping, or an element in a sequence.
    """
    @abstractmethod
    def value(self) -> Any:
        "Get the value associated with this path component"

    def __eq__(self, other):
        return self.value() == other.value()

    def __repr__(self):
        return f"{type(self).__name__}(value={self.value()})"


YAMLPath = tuple[YAMLPathComponent, ...]


class Item(YAMLPathComponent):
    "A reference to a *key-value pair* in a mapping"
    def __init__(self, value: Any):
        self._value = value 

    def value(self) -> Any:
        "The key in the mapping."
        return self._value

    def __str__(self):
        return f"item/{self.value()}"

class Key(Item):
    "A reference to a *key* in a mapping"
    def __str__(self):
        return f"key/{self.value()}"


class Value(Item):
    "A reference to a *value* in a mapping"
    def __str__(self):
        return f"value/{self.value()}"


class Index(YAMLPathComponent):
    "A reference to the index-th element in a sequence"
    def __init__(self, index: int):
        self._index = index

    def value(self) -> int:
        return self._index

    def __str__(self):
        return f"index/{self._index}"

