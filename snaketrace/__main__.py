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
    parser.add_argument('--tsv', dest='output_format', action='store_const', const=trace.OutputFormat.TSV,
                        help='output as tab separated values')
    parser.add_argument('--color', choices=['never', 'always', 'auto'],
                        help='colorize output', default='auto')
    timefmt_group = parser.add_mutually_exclusive_group()
    timefmt_group.add_argument('-t', dest='timefmt', action='store_const', const=TIMEFMT_T,
                               help='print absolute timestamp')
    timefmt_group.add_argument('-tt', dest='timefmt', action='store_const', const=TIMEFMT_TT,
                               help='print absolute timestamp with usec')
    timefmt_group.add_argument('--timefmt', dest='timefmt',
                               help='print absolute timestamp with custom format')
    parser.add_argument('-e', '--filter', action='append',
                        help='filter audit events matching glob pattern (may be specified multiple times)')
    parser.add_argument('-o', '--output', help='write output to file with given name')
    parser.add_argument('-m', dest='is_module', action='store_true', help='run library module as script')
    parser.add_argument('name', help='Script or module to run')
    parser.add_argument('args', help='script arguments', nargs=argparse.REMAINDER)
    args = parser.parse_args()

    color = args.color == 'always' if args.color != 'auto' else None
    output = open(args.output, 'w') if args.output else None
    try:
        trace.trace(args.name, args.args, is_module=args.is_module, output=output, output_format=args.output_format,
                    filters=args.filter, color=color, timefmt=args.timefmt)
    finally:
        if output:
            output.close()


if __name__ == '__main__':
    main()
