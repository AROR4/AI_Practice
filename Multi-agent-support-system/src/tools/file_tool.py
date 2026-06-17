from pathlib import Path


def read_file(file_path: str) -> str:
    return Path(file_path).read_text()