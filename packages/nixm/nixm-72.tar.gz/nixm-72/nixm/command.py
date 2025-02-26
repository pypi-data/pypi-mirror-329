# This file is placed in the Public Domain.


"user commands"


import inspect
import os
import sys
import time
import types
import typing


from .find   import spl
from .object import Default
from .table  import Table, gettable
from .thread import launch


STARTTIME = time.time()


class Config(Default):

    init    = ""
    name    = __name__.split(".")[-2]
    opts    = Default()


class Commands:

    cmds = {}
    names = gettable()

    @staticmethod
    def add(func, mod=None) -> None:
        Commands.cmds[func.__name__] = func
        if mod:
            Commands.names[func.__name__] = mod.__name__

    @staticmethod
    def get(cmd) -> typing.Callable:
        return Commands.cmds.get(cmd, None)

    @staticmethod
    def getname(cmd) -> None:
        return Commands.names.get(cmd)

    @staticmethod
    def scan(mod) -> None:
        for key, cmdz in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmdz.__code__.co_varnames:
                Commands.add(cmdz, mod)


def command(evt) -> None:
    parse(evt)
    func = Commands.get(evt.cmd)
    if not func:
        name = Commands.names.get(evt.cmd)
        if name:
            mod = Table.load(name)
            func = getattr(mod, evt.cmd)
    if func:
        func(evt)
        evt.display()
    evt.ready()


def inits(pkg, names, pname) -> [types.ModuleType]:
    mods = []
    for name in modules(pkg.__path__[0]):
        if names and name not in spl(names):
            continue
        mname = pname + "." + name
        if not mname:
            continue
        mod = getattr(pkg, name, None)
        if not mod:
             continue
        if "init" in dir(mod):
           thr = launch(mod.init)
           mods.append((mod, thr))
    return mods


def modules(path) -> [str]:
    return [
            x[:-3] for x in os.listdir(path)
            if x.endswith(".py") and not x.startswith("__")
           ]


"utilities"


def parse(obj, txt=None) -> None:
    if txt is None:
        if "txt" in dir(obj):
            txt = obj.txt
        else:
            txt = ""
    args = []
    obj.args    = []
    obj.cmd     = ""
    obj.gets    = Default()
    obj.index   = None
    obj.mod     = ""
    obj.opts    = ""
    obj.result  = {}
    obj.sets    = Default()
    obj.txt     = txt or ""
    obj.otxt    = obj.txt
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""


def scan(pkg, mods=""):
    res = []
    path = pkg.__path__[0]
    pname = pkg.__name__
    for nme in modules(path):
        if "__" in nme:
            continue
        if mods and nme not in spl(mods):
            continue
        name = pname + "." + nme
        if not name:
            continue
        mod = getattr(pkg, nme, None)
        if not mod:
            continue
        Commands.scan(mod)
        res.append(mod)
    return res


def __dir__():
    return (
        'STARTTIME',
        'Commands',
        'command',
        'inits',
        'parse',
        'scan',
        'spl'
    )
