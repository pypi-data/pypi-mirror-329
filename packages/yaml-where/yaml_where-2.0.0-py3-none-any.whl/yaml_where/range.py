"""Basic types for representing positions and ranges in a document."""

from dataclasses import dataclass
from ruamel.yaml.nodes import Node


@dataclass(frozen=True)
class Position:
    "Zero-based indexes describing a position in a document."
    line: int
    column: int

    def __lt__(self, other):
        "Check if this position is before another."
        return (self.line, self.column) < (other.line, other.column)

    def __le__(self, other):
        "Check if this position is before another."
        return (self.line, self.column) <= (other.line, other.column)


@dataclass(frozen=True)
class Range:
    "Half-open range describing a span inside a document."
    start: Position
    end: Position


    def __post_init__(self):
        if not self.start <= self.end:
            raise ValueError(f"Range start ({self.start}) must be before end ({self.end}).")

    def __le__(self, other):
        "Check if this range is contained within another."
        return other.start <= self.start and self.end <= other.end

    def __contains__(self, pos: Position):
        "Check if a position is within this range."
        return self.start <= pos < self.end

    @classmethod
    def beginning(cls, length=1):
        "Create a range that starts at the beginning of the document."
        return cls(Position(0, 0), Position(0, length))

    @classmethod
    def from_node(cls, node: Node):
        "Create a range that covers the entire node."
        return cls(
            Position(node.start_mark.line, node.start_mark.column),
            Position(node.end_mark.line, node.end_mark.column),
        )

    @classmethod
    def from_parts(cls, start_line, start_column, end_line, end_column):
        "Create a range from its parts."
        return cls(Position(start_line, start_column), Position(end_line, end_column))