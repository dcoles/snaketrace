import argparse
import ctypes
import sys

from snaketrace import trace

TIMEFMT_T = '%H:%M:%S'
TIMEFMT_TT = '%H:%M:%S.%f'

def main():
    if sys.platform == 'win32':
        # Ensure ANSI/VT100 mode is enabled
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-12), 0x0007)

    parser = argparse.ArgumentParser(prog='snaketrace', description='Trace Python audit events')
    parser.add_argument('--color', choices=['never', 'always', 'auto'],
                        help='colorize output', default='auto')
    timefmt_group = parser.add_mutually_exclusive_group()
    timefmt_group.add_argument('-t', dest='timefmt', action='store_const', const=TIMEFMT_T,
                               help='print absolute timestamp')
    timefmt_group.add_argument('-tt', dest='timefmt', action='store_const', const=TIMEFMT_TT,
                               help='print absolute timestamp with usec')
    timefmt_group.add_argument('--timefmt', dest='timefmt',
                               help='print absolute timestamp with custom format')
    parser.add_argument('-e', '--filter', help='filter audit events matching glob pattern')
    parser.add_argument('-o', '--output', help='write output to file with given name')
    parser.add_argument('filename', help='Python script')
    parser.add_argument('args', help='Python script arguments', nargs='*')
    args = parser.parse_args()

    color = args.color == 'always' if args.color != 'auto' else None
    output = open(args.output, 'w') if args.output else None
    try:
        trace.trace(args.filename, args.args, output=output, filter=args.filter, color=color, timefmt=args.timefmt)
    finally:
        if output:
            output.close()


if __name__ == '__main__':
    main()
