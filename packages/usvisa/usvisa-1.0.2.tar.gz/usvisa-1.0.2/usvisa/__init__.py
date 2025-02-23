import os 

PACKAGE_ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(PACKAGE_ROOT,'VERSION')) as f:
    __version__ = f.read().strip()