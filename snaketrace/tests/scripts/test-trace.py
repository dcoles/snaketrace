import os

# Should generate `open('/dev/null', 'r+', ...)
open(os.devnull, 'r+').close()
