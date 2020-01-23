import argparse

from pytrace import trace


def main():
    parser = argparse.ArgumentParser(description='Trace Python audit events')
    parser.add_argument('-c', '--color', action='store_true', help='colorize output')
    parser.add_argument('-e', '--filter', help='filter audit events matching glob pattern')
    parser.add_argument('-o', '--output', help='write output to file with given name')
    parser.add_argument('filename', help='Python script')
    parser.add_argument('args', help='Python script arguments', nargs='*')
    args = parser.parse_args()

    output = open(args.output, 'w') if args.output else None
    try:
        trace.trace(args.filename, args.args, output=output, filter=args.filter, color=args.color)
    finally:
        if output:
            output.close()


if __name__ == '__main__':
    main()
