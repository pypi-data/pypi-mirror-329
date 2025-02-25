# This file is placed in the Public Domain.


"errors"


from nixt.excepts import Errors


def err(event):
    nmr = 0
    for line in Errors.errors:
        event.reply(line.strip())
        nmr += 1
    if not nmr:
        event.reply("no errors")
        return
    event.reply(f"found {nmr} errors.")
