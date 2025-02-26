import pathlib
import sys

import IPython

ip = IPython.get_ipython()
x = pathlib.Path(sys.argv[1]).resolve().read_text()
ip.set_next_input(x)
