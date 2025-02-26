"""Main implementation of source map calculation.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterable
from functools import singledispatch

from ruamel.yaml import YAML, MappingNode, Node, ScalarNode, SequenceNode
from yaml_where.exceptions import MissingKeyError, NoSuchPathError, UndefinedAccessError, UnsupportedNodeTypeError
from yaml_where.path import Index, Item, Key, YAMLPath, YAMLPathComponent, Value
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

    def get_path(self, pos: Position) -> YAMLPath:
        """Get the path corresponding to a position in the document.

        Args:
            pos (Position): The position to get the path for.

        Returns:
            Iterable[PathComponent]: The path components for the position.
        """
        return tuple(self._get_path(pos))

    @abstractmethod
    def _get_path(self, pos: Position) -> Iterable[YAMLPathComponent]:
        """Get the path corresponding to a Range."""

    @abstractmethod
    def get_range(self, *path: YAMLPathComponent) -> Range:
        """Get the range for an entire entry.

        Different subclasses will have different behaviors for this method. Mappings will return the range
        for the key-value pair, while sequences will return the range for the sequence element.

        Raises:
            MissingKeyError: A key is of the appropriate type for an element, but is missing in that elements. For
                example, if an integer index is beyond the end of a sequence element.

            UndefinedAccessError: If a key is of an inappropriate type for an element. For example, if a string is
                used to access a sequence element.
        """

class YAMLWhereScalar(YAMLWhere):
    "Source map calculator for scalar nodes."

    def __init__(self, node: ScalarNode):
        if not isinstance(node, ScalarNode):
            raise ValueError(f"YAMLWhereScalar can not be constructed with a {type(node).__name__}")
        super().__init__(node)

    def _get_path(self, rng: Range) -> Iterable[YAMLPathComponent]:
        return []

    def get_range(self, *path: YAMLPathComponent) -> Range:
        if path:
            raise UndefinedAccessError("get_range() path must be empty for scalars")

        return Range.from_node(self.node)


class YAMLWhereSequence(YAMLWhere):
    "Source map calculator for sequence nodes."

    def __init__(self, node: SequenceNode):
        if not isinstance(node, SequenceNode):
            raise ValueError(
                f"YAMLWhereSequence can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def _get_path(self, pos: Position) -> Iterable[YAMLPathComponent]:
        for idx, child in enumerate(self.node.value):
            if pos in Range.from_node(child):
                yield Index(idx)
                yield from _from_node(child).get_path(pos)
                return
        raise NoSuchPathError(f"Can not resolve the range {pos} to a path in {self.node.value}")

    def get_range(self, *path: YAMLPathComponent) -> Range:
        if not path:
            raise UndefinedAccessError(
                "get_range() with empty path is not defined for sequence elements"
            )

        head, tail = path[0], path[1:]

        if not isinstance(head, Index):
            raise UndefinedAccessError(f"Can not access a sequence with non-index component {head}")

        try:
            value_node = self.node.value[head.value()]
        except IndexError as err:
            raise MissingKeyError(head) from err

        if tail:
            return _from_node(value_node).get_range(*tail)

        return Range.from_node(value_node)


class YAMLWhereMapping(YAMLWhere):
    "Source map calculator for mapping nodes."

    def __init__(self, node: MappingNode):
        if not isinstance(node, MappingNode):
            raise ValueError(
                f"YAMLWhereMapping can not be constructed with a {type(node).__name__}"
            )

        super().__init__(node)

    def _get_path(self, pos: Position) -> Iterable[YAMLPathComponent]:
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

    def get_range(self, *path: YAMLPathComponent) -> Range:
        if not path:
            raise UndefinedAccessError(
                "get_range() with no arguments is not defined for sequence elements"
            )

        head, tail = path[0], path[1:]

        if not isinstance(head, Item):
            raise UndefinedAccessError(f"Can not access a mapping with non-item component {head}")

        for child_key, child_value in self.node.value:
            if child_key.value == head.value():
                if tail:
                    return _from_node(child_value).get_range(*tail)

                elif isinstance(head, Key):
                    return Range.from_node(child_key)

                elif isinstance(head, Value):
                    return Range.from_node(child_value)

                else: 
                    assert isinstance(head, Item)
                    return Range(
                        Position(child_key.start_mark.line, child_key.start_mark.column),
                        Position(child_value.end_mark.line, child_value.end_mark.column),
                    )

        raise MissingKeyError(head)


class YAMLWhereNull(YAMLWhere):
    "Source map calculator for null nodes."

    def _get_path(self, pos: Position) -> Iterable[YAMLPathComponent]:
        raise NoSuchPathError("Can not resolve a path in a null node")

    def get_range(self, *path) -> Range:
        raise UndefinedAccessError("get() is not defined for null nodes")


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

