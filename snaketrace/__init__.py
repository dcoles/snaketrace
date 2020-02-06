import sys

# Clean module state
MODULES = dict((m for m in sys.modules.items() if m[0] is not __name__))
