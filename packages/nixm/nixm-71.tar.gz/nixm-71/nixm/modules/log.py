# This file is placed in the Public Domain.


"log text"


import time


from nixt.disk   import ident, write
from nixt.find   import find, fntime, store
from nixt.object import Object


from .command  import elapsed


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''


def log(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('log'):
            lap = elapsed(time.time() - fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply('no log')
        return
    obj = Log()
    obj.txt = event.rest
    write(obj, store(ident(obj)))
    event.done()


def __dir__():
    return (
        'log',
    )
