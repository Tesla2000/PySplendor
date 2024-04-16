import importlib
from itertools import count
from pathlib import Path

__all__ = [
    (module.with_suffix("").name, importlib.import_module("." + module.with_suffix("").name, __name__))[0]
    for module in Path(__file__).parent.iterdir()
    if module.name not in ("__init__.py", "pycache")
]

from time import sleep

from tqdm import tqdm

from db.Base import Base
from db.engine import engine

for _ in tqdm(count()):
    try:
        Base.metadata.create_all(engine)
        break
    except:
        sleep(1)
