#!/bin/python3

__all__ = ['cmdline', 'cmdline_default', 'cmdline_start',
           'optfunc', 'optfunc_default', 'optfunc_start', 'called_directly']

import atexit
from optfunc2.parser import cmdline as cmdline
from optfunc2.parser import cmdline_default as cmdline_default
from optfunc2.parser import cmdline_start as cmdline_start

from optfunc2.parser import cmdline as optfunc
from optfunc2.parser import cmdline_default as optfunc_default
from optfunc2.parser import cmdline_start as optfunc_start
from .parser import called_directly
