# SnakeTrace &#x1F40D;

An `strace`-like tool for [Python audit events](https://docs.python.org/3/library/audit_events.html#audit-events).

![Screenshot of SnakeTrace](https://user-images.githubusercontent.com/1007415/73980951-14640a80-48e6-11ea-932e-5a3212f59835.png)

## Requirements

- Python 3.8 or later

## Installation

Latest release via [`pip`](https://pip.pypa.io):

```bash
pip install snaketrace [--user]
```

via Git:

```bash
git clone https://github.com/dcoles/snaketrace.git; cd snaketrace
python3 setup.py install [--user]
```

## Usage

```
usage: snaketrace [-h] [--tsv] [--color {never,always,auto}] [-t | -tt | --timefmt TIMEFMT] [-e FILTER]
                  [-o OUTPUT]
                  script [args [args ...]]

Trace Python audit events

positional arguments:
  script                Python script
  args                  Python script arguments

optional arguments:
  -h, --help            show this help message and exit
  --tsv                 output as tab separated values
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
