"""Main implementation of source map calculation.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import singledispatch

from ruamel.yaml import YAML, MappingNode, Node, ScalarNode, SequenceNode
from yaml_where.exceptions import MissingKeyError, NoSuchPathError, UndefinedAccessError, UnsupportedNodeTypeError
from yaml_where.path import Index, Key, PathComponent, Value
from yaml_where.range import Position, Range


class YAMLWhere(ABC):
    """Base class for source map calculators for different YAML data types.

    This defines the interface for all source map calculators, but is itself abstract.
    """

    @classmethod
    def from_string(cls, source: str):
        """Create a YAMLWhere from a YAML string.

        Args:
            source (str): The YAML string to parse.

        Returns:
            YAMLWhere: The YAMLWhere instance with source map information.
        """
        y = YAML(typ="rt")
        node = y.compose(source)
        return _from_node(node)

    def __init__(self, node: Node):
        self.node = node

    def get_path(self, pos: Position) -> tuple[PathComponent, ...]:
        """Get the path corresponding to a position in the document.

        Args:
            pos (Position): The position to get the path for.

        Returns:
            Iterable[PathComponent]: The path components for the position.
        """
        return tuple(self._get_path(pos))

    @abstractmethod
    def _get_path(self, pos: Position) -> Iterable[PathComponent]:
        """Get the path corresponding to a Range."""

    @abstractmethod
    def get_range(self, *keys: str | int) -> Range:
        """Get the range for an entire entry.

        Different subclasses will have different behaviors for this method. Mappings will return the range
        for the key-value pair, while sequences will return the range for the sequence element.

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element.
        """

    @abstractmethod
    def get_key_range(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a mapping key.

        So for a mapping, this would return the range for the key in the key-value pair.

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element. Or if 'key' is no a defined concept for the element.
        """

    @abstractmethod
    def get_value_range(self, key: str | int, *keys: str | int) -> Range:
        """Get the range for a value.

        For a mapping this gets the range of the value in the key-value pair. For a sequence this gets the range
        of the sequence element (just like get()).

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.
            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element. Or if 'key' is no a defined concept for the element.
        """



class YAMLWhereScalar(YAMLWhere):
    "Source map calculator for scalar nodes."

    def __init__(self, node: ScalarNode):
        if not isinstance(node, ScalarNode):
            raise ValueError(f"YAMLWhereScalar can not be constructed with a {type(node).__name__}")
        super().__init__(node)

    def _get_path(self, rng: Range) -> Iterable:
        return []

    def get_range(self, *keys: str | int) -> Range:
        if keys:
            raise UndefinedAccessError("get() with no arguments is not defined for scalar nodes")

        return Range.from_node(self.node)

    def get_key_range(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_key() is not defined for scalar nodes")

    def get_value_range(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_value() is not defined for scalar nodes")


class YAMLWhereSequence(YAMLWhere):
    "Source map calculator for sequence nodes."

    def __init__(self, node: SequenceNode):
        if not isinstance(node, SequenceNode):
            raise ValueError(
                f"YAMLWhereSequence can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def _get_path(self, pos: Position) -> Iterable:
        for idx, child in enumerate(self.node.value):
            if pos in Range.from_node(child):
                yield Index(idx)
                yield from _from_node(child).get_path(pos)
                return
        raise NoSuchPathError(f"Can not resolve the range {pos} to a path in {self.node.value}")

    def get_range(self, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError(
                "get() with no arguments is not defined for sequence elements"
            )

        key, keys = keys[0], keys[1:]

        if not isinstance(key, int):
            raise UndefinedAccessError(f"Can not access a sequence with non-integer key {key}")

        if keys:
            return _from_node(self.node.value[key]).get_range(*keys)

        try:
            value_node = self.node.value[key]
        except IndexError as err:
            raise MissingKeyError(key) from err

        return Range.from_node(value_node)

    def get_key_range(self, key: str | int, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError("get_key() is not defined for sequence elements")

        return _from_node(self.node.value[key]).get_key_range(*keys)

    def get_value_range(self, key: str | int, *keys: str | int) -> Range:
        if not isinstance(key, int):
            raise UndefinedAccessError(f"Can not access a sequence with non-integer key {key}")

        if keys:
            return _from_node(self.node.value[key]).get_value_range(*keys)

        try:
            value_node = self.node.value[key]
        except IndexError as err:
            raise MissingKeyError(key) from err

        return Range.from_node(value_node)


class YAMLWhereMapping(YAMLWhere):
    "Source map calculator for mapping nodes."

    def __init__(self, node: MappingNode):
        if not isinstance(node, MappingNode):
            raise ValueError(
                f"YAMLWhereMapping can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def _get_path(self, pos: Position) -> Iterable[PathComponent]:
        for key_node, value_node in self.node.value:
            # Check if we're looking at the key
            if pos in Range.from_node(key_node):
                yield Key(key_node.value)
                # yield from _from_node(value_node).get_path(pos)
                return

            elif pos in Range.from_node(value_node):
                yield Value(key_node.value)
                yield from _from_node(value_node).get_path(pos)
                return

        raise NoSuchPathError(f"Can not resolve the range {pos} to a path in {self.node.value}")

    def get_range(self, *keys: str | int) -> Range:
        if not keys:
            raise UndefinedAccessError(
                "get() with no arguments is not defined for sequence elements"
            )

        key, keys = keys[0], keys[1:]

        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range(
                        Position(child_key.start_mark.line, child_key.start_mark.column),
                        Position(child_value.end_mark.line, child_value.end_mark.column),
                    )
                else:
                    return _from_node(child_value).get_range(*keys)

        raise MissingKeyError(key)

    def get_key_range(self, key: str | int, *keys: str | int) -> Range:
        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range.from_node(child_key)
                else:
                    return _from_node(child_value).get_key_range(*keys)

        raise MissingKeyError(key)

    def get_value_range(self, key: str | int, *keys: str | int) -> Range:
        for child_key, child_value in self.node.value:
            if child_key.value == key:
                if not keys:
                    return Range.from_node(child_value)
                else:
                    return _from_node(child_value).get_value_range(*keys)

        raise MissingKeyError(key)


class YAMLWhereNull(YAMLWhere):
    "Source map calculator for null nodes."

    def _get_path(self, pos: Position) -> Iterable:
        raise NoSuchPathError("Can not resolve a path in a null node")

    def get_range(self, *keys: str | int) -> Range:
        raise UndefinedAccessError("get() is not defined for null nodes")

    def get_key_range(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_key() is not defined for null nodes")

    def get_value_range(self, key: str | int, *keys: str | int) -> Range:
        raise UndefinedAccessError("get_value() is not defined for null nodes")


@singledispatch
def _from_node(node: Node) -> YAMLWhere:
    "Construct a YAMLWhere based on the type of the node."
    raise UnsupportedNodeTypeError(
        f"Unsupported node type {type(node).__name__}"
    )  # pragma: no cover


@_from_node.register(ScalarNode)
def _(node):
    return YAMLWhereScalar(node)


@_from_node.register(MappingNode)
def _(node):
    return YAMLWhereMapping(node)


@_from_node.register(SequenceNode)
def _(node):
    return YAMLWhereSequence(node)


@_from_node.register(type(None))
def _(node):
    return YAMLWhereNull(node)

