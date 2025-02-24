from abc import abstractmethod
from typing import Any


class PathComponent:
    @abstractmethod
    def value(self) -> Any:
        "Get the value associated with this path component"

    def __eq__(self, other):
        return self.value() == other.value()

    def __repr__(self):
        return f"{type(self).__name__}(value={self.value()})"


class Key(PathComponent):
    def __init__(self, value: str):
        self._value = value

    def value(self) -> str:
        return self._value

    def __str__(self):
        return f"key/{self.value()}"


class Value(PathComponent):
    def __init__(self, value: Any):
        self._value = value 

    def value(self) -> Any:
        return self._value

    def __str__(self):
        return f"value/{self.value()}"


class Index(PathComponent):
    def __init__(self, index: int):
        self._index = index

    def value(self) -> int:
        return self._index

    def __str__(self):
        return f"index/{self._index}"

