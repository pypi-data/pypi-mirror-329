# This file is placed in the Public Domain.


"fleet"


from nixt.objects import fmt
from nixt.reactor import Fleet
from nixt.threads import name


def flt(event):
    bots = Fleet.bots.values()
    try:
        event.reply(fmt(list(Fleet.bots.values())[int(event.args[0])]))
    except (KeyError, IndexError, ValueError):
        event.reply(",".join([name(x).split(".")[-1] for x in bots]))
