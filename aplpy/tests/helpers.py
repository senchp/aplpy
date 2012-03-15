import string
import random
import os

import pyfits
import pywcs
import numpy as np

import sys
import shlex
import base64
import zlib
import subprocess

from distutils.core import Command

# Load local pytest

from ..extern import pytest as extern_pytest

if sys.version_info >= (3, 0):
    exec("def do_exec_def(co, loc): exec(co, loc)\n")
    extern_pytest.do_exec = do_exec_def

    import pickle
    unpacked_sources = extern_pytest.sources.encode("ascii")
    unpacked_sources = pickle.loads(
        zlib.decompress(base64.decodebytes(unpacked_sources)))
else:
    exec("def do_exec_def(co, loc): exec co in loc\n")
    extern_pytest.do_exec = do_exec_def

    import cPickle as pickle
    unpacked_sources = pickle.loads(
        zlib.decompress(base64.decodestring(extern_pytest.sources)))

importer = extern_pytest.DictImporter(unpacked_sources)
sys.meta_path.append(importer)

pytest = importer.load_module('pytest')


class TestRunner(object):

    def __init__(self, base_path):
        self.base_path = base_path

    def run_tests(self, args=None, plugins=None, verbose=False,
                  pastebin=None):
        """
        Run tests using py.test. A proper set of arguments is constructed and
        passed to `pytest.main`.

        Parameters
        ----------
        args : str, optional
            Additional arguments to be passed to `pytest.main` in the `args`
            keyword argument.

        plugins : list, optional
            Plugins to be passed to `pytest.main` in the `plugins` keyword
            argument.

        verbose : bool, optional
            Convenience option to turn on verbose output from py.test. Passing
            True is the same as specifying `-v` in `args`.

        pastebin : {'failed','all',None}, optional
            Convenience option for turning on py.test pastebin output. Set to
            'failed' to upload info for failed tests, or 'all' to upload info
            for all tests.

        See Also
        --------
        pytest.main : py.test function wrapped by `run_tests`.

        """

        all_args = self.base_path

        # add any additional args entered by the user
        if args is not None:
            all_args += ' {0}'.format(args)

        # add verbosity flag
        if verbose:
            all_args += ' -v'

        # turn on pastebin output
        if pastebin is not None:
            if pastebin in ['failed', 'all']:
                all_args += ' --pastebin={0}'.format(pastebin)
            else:
                raise ValueError("pastebin should be 'failed' or 'all'")

        all_args = shlex.split(all_args,
                               posix=not sys.platform.startswith('win'))

        return pytest.main(args=all_args, plugins=plugins)


class test_command(Command, object):
    user_options = [
        ('verbose-results', 'V',
         'Turn on verbose output from pytest. Same as specifying `-v` in '
         '`args`.'),
        ('plugins=', 'p',
         'Plugins to enable when running pytest.  Same as specifying `-p` in '
         '`args`.'),
        ('pastebin=', 'b',
         "Enable pytest pastebin output. Either 'all' or 'failed'."),
        ('args=', 'a', 'Additional arguments to be passed to pytest'),
    ]

    package_name = None

    def initialize_options(self):
        self.package = None
        self.test_path = None
        self.verbose_results = False
        self.plugins = None
        self.pastebin = None
        self.args = None

    def finalize_options(self):
        pass

    def run(self):

        self.reinitialize_command('build')
        self.run_command('build')
        build_cmd = self.get_finalized_command('build')
        new_path = os.path.abspath(build_cmd.build_lib)

        cmd = ('import aplpy, sys; sys.exit(aplpy.test(%s, %s, %s, %s))')
        args = (self.args, self.plugins, self.verbose_results, self.pastebin)

        raise SystemExit(subprocess.call([sys.executable, '-c', cmd % args],
                                         cwd=new_path, close_fds=False))


def random_id():
    return string.join(random.sample(string.letters + string.digits, 16), '')


def generate_header(header_file):

    # Read in header
    header = pyfits.Header()
    header.fromTxtFile(header_file)

    return header


def generate_data(header_file):

    # Read in header
    header = generate_header(header_file)

    # Find shape of array
    shape = []
    for i in range(header['NAXIS']):
        shape.append(header['NAXIS%i' % (i + 1)])

    # Generate data array
    data = np.zeros(shape[::-1])

    return data


def generate_hdu(header_file):

    # Read in header
    header = generate_header(header_file)

    # Generate data array
    data = generate_data(header_file)

    # Generate primary HDU
    hdu = pyfits.PrimaryHDU(data=data, header=header)

    return hdu


def generate_wcs(header_file):

    # Read in header
    header = generate_header(header_file)

    # Compute WCS object
    wcs = pywcs.WCS(header)

    return wcs


def generate_file(header_file, directory):

    # Generate HDU object
    hdu = generate_hdu(header_file)

    # Write out to a temporary file in the specified directory
    filename = os.path.join(directory, random_id() + '.fits')
    hdu.writeto(filename)

    print filename

    return filename
