#!/usr/bin/env python


from pathlib import Path

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError(
        'Could not import "setuptools".' "Please install the setuptools package."
    )


README = Path("./README.md")
LICENSE = """MIT License

Copyright (c) 2021 somenzz

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


# Read the version without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = "0.6"

NAME = "dbinterface"
VERSION = version
DESCRIPTION = ""
KEYWORDS = "python database client interface"
AUTHOR = "somenzz"
AUTHOR_EMAIL = "somenzz@163.com"
URL = "https://github.com/somenzz/dbinterface"
PACKAGES = find_packages(exclude=["tests", "tests.*"])

INSTALL_REQUIRES = []
TEST_SUITE = "tests"
TESTS_REQUIRE = []

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]


params = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "keywords": KEYWORDS,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "url": URL,
    "license": "MIT",
    "packages": PACKAGES,
    "install_requires": INSTALL_REQUIRES,
    "tests_require": TESTS_REQUIRE,
    "test_suite": TEST_SUITE,
    "classifiers": CLASSIFIERS,
    "long_description": README.read_text(),
}

if __name__ == "__main__":
    setup(**params, long_description_content_type="text/markdown")
