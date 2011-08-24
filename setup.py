#!/usr/bin/env python

from distutils.core import setup

try:  # Python 3.x
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:  # Python 2.x
    from distutils.command.build_py import build_py

setup(name='APLpy',
      version='0.9.6-userwcs',
      description='The Astronomical Plotting Library in Python',
      author='Thomas Robitaille, Eli Bressert, and Adam Ginsburg',
      author_email='thomas.robitaille@gmail.com, elibre@users.sourceforge.net, adam.g.ginsburg@gmail.com',
      license='MIT',
      url='http://aplpy.github.com/',
      download_url='https://github.com/downloads/aplpy/aplpy/APLpy.0.9.6.userwcs.tar.gz',
      packages=['aplpy'],
      provides=['aplpy'],
      requires=['pywcs', 'pyfits', 'numpy', 'matplotlib'],
      cmdclass={'build_py': build_py},
      keywords=['Scientific/Engineering'],
      classifiers=[
                   "Development Status :: 3 - Alpha",
                   "Programming Language :: Python",
                   "License :: OSI Approved :: MIT License",
                  ],
     )
