# SnakeTrace &#x1F40D;

An `strace`-like tool for [Python audit events](https://docs.python.org/3/library/audit_events.html#audit-events).

## Requirements

- Python 3.8 or later

## Installation

```bash
python3 setup.py install [--user]
```

## Usage

```
usage: snaketrace [-h] [--color {never,always,auto}] [-t | -tt | --timefmt TIMEFMT] [-e FILTER] [-o OUTPUT]
                  filename [args [args ...]]

Trace Python audit events

positional arguments:
  filename              Python script
  args                  Python script arguments

optional arguments:
  -h, --help            show this help message and exit
  --color {never,always,auto}
                        colorize output
  -t                    print absolute timestamp
  -tt                   print absolute timestamp with usec
  --timefmt TIMEFMT     print absolute timestamp with custom format
  -e FILTER, --filter FILTER
                        filter audit events matching glob pattern (may be specified multiple times)
  -o OUTPUT, --output OUTPUT
                        write output to file with given name
``` 

# License

Licensed under the [MIT License](/LICENSE).
