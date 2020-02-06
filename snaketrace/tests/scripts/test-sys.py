# Expected to be called as `test-sys.py foo -m bar baz`
import sys

assert 'sys' in sys.modules
assert sys.argv[1:] == ['foo', '-m', 'bar', 'baz']
