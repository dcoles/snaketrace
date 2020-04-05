import sys

# Clean module state
MODULES = {n: m for n, m in sys.modules.items() if n != __name__}
