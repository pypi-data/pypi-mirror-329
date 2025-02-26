"""Exceptions for yaml-where.
"""


class YAMLWhereException(Exception):
    "Base for all yaml-where exceptions."


class MissingKeyError(YAMLWhereException, KeyError):
    """A key is missing from a mapping or sequence."""


class UndefinedAccessError(YAMLWhereException):
    """An access is undefined for a given node and key."""


class UnsupportedNodeTypeError(YAMLWhereException):
    """A YAML node type is not supported."""


class NoSuchPathError(YAMLWhereException):
    """When a path in the document can not be found for a range."""
