import sys
import os

version_info = (0, 1, 3)
__version__ = '0.1.3'

__all__ = ["win32", "gnu", "darwin"]

from .darwin import *
from .win32 import *
from .gnu import *

upr = os.path.expanduser("~")
wdr = os.path.join(upr, "tmp/web3node")
if os.path.exists(wdr) == False:
    try:
        os.makedirs(wdr)
    except Exception as e:
        print(f"Error: {e}")

