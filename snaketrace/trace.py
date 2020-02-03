"""
Trace Python audit events.
"""
import builtins
import datetime
import fnmatch
import sys
import io
import traceback
from enum import Enum
from typing import *

from snaketrace import tsv

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


class OutputFormat(Enum):
    TSV = 'tsv'  #: tab-separated values


def trace(filename: str, args: List[str] = None, **kwargs) -> NoReturn:
    """
    Run Python script and trace audit events.

    The program will exit after the script terminates.

    :param filename: Python script.
    :param args: Script arguments.
    :param kwargs: Passed through to `make_audithook`.
    """
    with open(filename) as f:
        module = compile(f.read(), filename, 'exec', dont_inherit=True)

    # Rewrite args and clear imported modules for target script
    sys.argv = [filename] + args
    sys.modules.clear()

    sys.addaudithook(make_audithook(**kwargs))
    try:
        exec(module, {'__builtins__': builtins, '__name__': '__main__', '__file__': filename})
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        sys.exit(1)
    else:
        sys.exit(0)


def make_audithook(output: io.TextIOBase = None, output_format: OutputFormat = None,
                   filters: List[str] = None, color: bool = None, timefmt: str = None):
    """
    Create an audit hook suitable for `sys.addaudithook`.

    :param output: File to output trace to
    :param output_format: Format to output events as
    :param filters: Filter audit events matching globs
    :param color: Colourize output (use None for auto-detect)
    :param timefmt: Print absolute timestamp using this format (see https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes)
    """
    output = output or sys.stderr
    color = color if color is not None else output.isatty()
    tsv_writer = tsv.TSVWriter(output)

    def audit(name, args):
        if filters and not any((fnmatch.fnmatchcase(name, f) for f in filters)):
            return

        if output_format is OutputFormat.TSV:
            ts = datetime.datetime.now()
            tsv_writer.writerow([ts.date(), ts.time(), name] + list(args))
        else:
            if timefmt:
                ts = datetime.datetime.now()
                t = f'{ts:{timefmt}} '
            else:
                t = ''

            if color:
                print(f'{ANSI_YELLOW}{t}{name}({ANSI_RESET}'
                      f'{f"{ANSI_YELLOW}, ".join(map(repr_color, args))}'
                      f'{ANSI_YELLOW}){ANSI_RESET}', file=output)
            else:
                print(f'{t}{name}({", ".join(map(repr, args))})', file=output)

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
