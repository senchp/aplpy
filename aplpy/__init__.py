from .aplpy import FITSFigure
from .rgb import make_rgb_image, make_rgb_cube

# Testing framework copied from Astropy
from .tests.helpers import TestRunner
_test_runner = TestRunner(__path__[0])
del TestRunner
test = _test_runner.run_tests

__version__ = '0.9.7'
