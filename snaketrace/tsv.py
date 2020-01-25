import csv

# Escaped characters in TSV output
TSV_ESCAPE_TRANS = str.maketrans({
    '\r': r'\r',
    '\n': r'\n',
    '\t': r'\t',
    '\\': r'\\',
})


class TSV(csv.Dialect):
    """Tab-separated values."""
    delimiter = '\t'
    lineterminator = '\n'
    quoting = csv.QUOTE_NONE


class TSVWriter:
    """Writer for Tab-separated values with escaped special characters"""
    def __init__(self, fileobj):
        self._writer = csv.writer(fileobj, TSV)

    def writerow(self, row):
        """Write row with special characters escaped"""
        self._writer.writerow((str(v).translate(TSV_ESCAPE_TRANS) for v in row))
