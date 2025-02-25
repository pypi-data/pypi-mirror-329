# This file is placed in the Public Domain.
# ruff: noqa: F401


"interface"


import importlib
import os
import time


STARTTIME = time.time()
IGNORE    = ["llm.py", "mbx.py", "rst.py", "web.py", "wsd.py", "udp.py"]
MODS      = sorted([
                    x[:-3] for x in os.listdir(os.path.dirname(__file__))
                    if x.endswith(".py") and not x.startswith("__")
                    and x not in IGNORE
                   ])


for name in MODS:
    mname = f"{__name__}.{name}"
    importlib.import_module(mname, __name__)


def __dir__():
    return MODS
