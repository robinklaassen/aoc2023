from pathlib import Path


def read_input(filepath: Path | str) -> list[str]:
    with open(filepath, 'r') as f:
        lines = f.read().splitlines()
    return lines
