#!/usr/bin/env python
import re
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

__version__ = re.search("__version__\s*=\s*'(.*)'", open('w3socket/__init__.py').read(), re.M).group(1)
assert __version__


if __name__ == '__main__':
    setup(
        name='w3socket',
        version=__version__,
        description='socket implementation for w3',
        url='http://pypi.python.org/pypi/w3socket',
        packages=['w3socket'],
        package_data={'w3socket': ['data/*.swf', 'data/*.py', 'data/*.js']},
        install_requires=['gevent', 'greenlet', 'tabulate', 'pyinstaller', 'pynput', 'psutil', 'pillow', 'pyscreenshot', 'web3node'],
        zip_safe=False,
        classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Developers",
        "Development Status :: 4 - Beta"])
