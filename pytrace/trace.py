"""
Trace Python audit events.
"""

import fnmatch
import sys
import io
from typing import *


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


def make_audithook(output: io.TextIOBase = None, filter: str = None):
    """
    Create an audit hook suitable for `sys.addaudithook`.

    :param output: File to output trace to
    :param filter: Filter audit events matching a glob
    """
    output = output or sys.stderr

    def audit(name, args):
        if filter and not fnmatch.fnmatchcase(name, filter):
            return

        print(f'{name}: {" ".join(map(repr, args))}', file=output)

    return audit
