from yaml_where.range import Position, Range


def clean_yaml(s: str) -> str:
    lines = s.split("\n")
    min_indent = min(len(line) - len(line.lstrip()) for line in lines if line.strip())

    trimmed = [line[min_indent:] for line in lines]
    if trimmed[0] == "":
        trimmed = trimmed[1:]
    if trimmed[-1] == "":
        trimmed = trimmed[:-1]

    return "\n".join(trimmed)


def extent(start_line: int, start_col: int, length: int):
    return Range.from_parts(start_line, start_col, start_line, start_col + length)
