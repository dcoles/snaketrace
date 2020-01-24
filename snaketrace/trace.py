"""
Trace Python audit events.
"""

import fnmatch
import sys
import io
from typing import *

# ANSI terminal escape codes (https://en.wikipedia.org/wiki/ANSI_escape_code#Colors)
ANSI_RED = '\x1b[95m'
ANSI_GREEN = '\x1b[32m'
ANSI_YELLOW = '\x1b[33m'
ANSI_BLUE = '\x1b[34m'
ANSI_MAGENTA = '\x1b[35m'
ANSI_CYAN = '\x1b[36m'
ANSI_BMAGENTA = '\x1b[95m'
ANSI_RESET = '\x1b[0m'

# Mapping of types to colours
COLORMAP = {
    str: ANSI_BMAGENTA,
    bytes: ANSI_BMAGENTA,
    int: ANSI_GREEN,
    float: ANSI_GREEN,
    type(None): ANSI_MAGENTA,
}


def trace(filename: str, args: List[str] = None, **kwargs):
    """
    Run Python script and trace audit events.

    :param filename: Python script.
    :param args: Script arguments.
    :param kwargs: Passed through to `make_audithook`.
    """
    with open(filename) as f:
        program = compile(f.read(), filename, 'exec', dont_inherit=True)

    # Rewrite `argv` for target script
    old_argv = sys.argv
    sys.argv = [filename] + args
    try:
        sys.addaudithook(make_audithook(**kwargs))
        exec(program)
    finally:
        # Restore `argv`
        sys.argv = old_argv


def make_audithook(output: io.TextIOBase = None, filter: str = None, color = False):
    """
    Create an audit hook suitable for `sys.addaudithook`.

    :param output: File to output trace to
    :param filter: Filter audit events matching a glob
    :param color: Colourize output
    """
    output = output or sys.stderr

    def audit(name, args):
        if filter and not fnmatch.fnmatchcase(name, filter):
            return

        if color and output.isatty():
            print(f'{ANSI_YELLOW}{name}({ANSI_RESET}'
                  f'{f"{ANSI_YELLOW}, ".join(map(repr_color, args))}'
                  f'{ANSI_YELLOW}){ANSI_RESET}', file=output)
        else:
            print(f'{name}({", ".join(map(repr, args))})', file=output)

    return audit


def repr_color(obj):
    if isinstance(obj, list):
        return f'{ANSI_BLUE}[{f"{ANSI_BLUE}, ".join(map(repr_color, obj))}{ANSI_BLUE}]{ANSI_RESET}'
    elif isinstance(obj, dict):
        return f'{ANSI_BLUE}{{' \
               f'{f"{ANSI_BLUE}, ".join((f"{repr_color(k)}{ANSI_BLUE}: {repr_color(v)}" for k, v in obj.items()))}' \
               f'{ANSI_BLUE}}}{ANSI_RESET}'
    else:
        color = COLORMAP.get(type(obj), ANSI_CYAN)
        return f'{color}{obj!r}{ANSI_RESET}'
