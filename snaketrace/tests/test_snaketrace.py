import os
import re
from pathlib import Path
import sys
import unittest
import subprocess

BASEDIR = Path(__file__).parent


def snaketrace(script, *args, extra=None, capture_output=False):
    """
    Run snaketrace in subprocess.

    Because audit hooks can't be removed, we have to run each test in its
    own dedicated process.

    :param script: Script to run
    :param args: Script arguments
    :param extra: Additional arguments to snaketrace
    :param capture_output: Should we capture output
    :return: `subprocess.CompletedProcess`
    """
    extra = extra or []
    output = ['-o', os.devnull] if not capture_output else []
    return subprocess.run(
        [sys.executable, '-m', 'snaketrace', *output, *extra, script, *args],
        cwd=BASEDIR, capture_output=capture_output, encoding='utf-8', check=True)


class TestTrace(unittest.TestCase):

    def test_env(self):
        snaketrace('scripts/test-env.py')

    def test_sys(self):
        # Script is expected to be called as `test-sys.py foo -m bar baz`
        snaketrace('scripts/test-sys.py', 'foo', '-m', 'bar', 'baz')

    def test_trace(self):
        p = snaketrace('scripts/test-trace.py', capture_output=True)

        assert f"\nopen({os.devnull!r}, 'r+', " in p.stderr, f'Got:\n{p.stderr}'
        assert re.search(r'^exec\(<code object <module> at 0x\w+, file "scripts/test-trace\.py", line 1>\)$', p.stderr, flags=re.MULTILINE)

    def test_trace_filter_glob(self):
        p = snaketrace('scripts/test-trace.py', extra=['-e', 'ope?'], capture_output=True)

        assert all((line.startswith('open(') for line in p.stderr.splitlines())), f'Got:\n{p.stderr}'

    def test_trace_filter_multi(self):
        # Should match prefix 'ope'
        p = snaketrace('scripts/test-trace.py', extra=['-e', 'open', '-e', 'exec'], capture_output=True)

        assert '\nopen(' in p.stderr
        assert '\nexec(' in p.stderr
        assert all((line.startswith('open(') or line.startswith('exec') for line in p.stderr.splitlines())), f'Got:\n{p.stderr}'

    def test_trace_t(self):
        p = snaketrace('scripts/test-trace.py', extra=['-t'], capture_output=True)

        assert all((re.match(r'\d{2}:\d{2}:\d{2} \S+\(', line) for line in p.stderr.splitlines())), f'Got:\n{p.stderr}'

    def test_trace_tt(self):
        p = snaketrace('scripts/test-trace.py', extra=['-tt'], capture_output=True)

        assert all((re.match(r'\d{2}:\d{2}:\d{2}\.\d{6} \S+\(', line) for line in p.stderr.splitlines())), f'Got:\n{p.stderr}'

    def test_trace_timefmt(self):
        p = snaketrace('scripts/test-trace.py', extra=['--timefmt', 'x%Yx'], capture_output=True)

        assert all((re.match(r'x\d{4}x \S+\(', line) for line in p.stderr.splitlines())), f'Got:\n{p.stderr}'

    def test_trace_csv(self):
        p = snaketrace('scripts/test-trace.py', extra=['--tsv'], capture_output=True)

        pattern = r'^\d{4}-\d{2}-\d{2}\t\d{2}:\d{2}:\d{2}\.\d{6}\topen\t' + os.devnull + r'\tr\+\t\d+$'
        assert re.search(pattern, p.stderr, flags=re.MULTILINE), f'Got:\n{p.stderr}'
