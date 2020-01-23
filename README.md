# PyTrace

An `strace`-like tool for [Python audit events](https://docs.python.org/3/library/audit_events.html#audit-events).

## Requirements

- Python 3.8 or newer

## Installation

```bash
python3 setup.py install [--user]
```

## Usage

```
usage: pytrace [-h] [-o OUTPUT] [-e FILTER] file [args [args ...]]

Trace Python audit events

positional arguments:
  file                  Python script
  args                  Python script arguments

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        write output to file with given name
  -e FILTER, --filter FILTER
                        filter audit events matching glob pattern
``` 

# License

Licensed under the [MIT License](/LICENSE).
