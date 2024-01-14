from contextlib import contextmanager
from pathlib import Path

DATA_DIR = Path(__file__).parent / "resources"


@contextmanager
def load(path):
    with open(DATA_DIR / path) as data:
        yield data
