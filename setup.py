#!/usr/bin/env python


from pathlib import Path

try:
    from setuptools import setup
    from setuptools import find_packages
except ImportError:
    raise ImportError(
        'Could not import "setuptools".' "Please install the setuptools package."
    )


README = Path("README.md")
LICENSE = Path("LICENSE")


# Read the version without importing the package
# (and thus attempting to import packages it depends on that may not be
# installed yet)
version = "0.2"

NAME = "dbinterface"
VERSION = version
DESCRIPTION = ""
KEYWORDS = "python database client interface"
AUTHOR = "somenzz"
AUTHOR_EMAIL = "somenzz@163.com"
URL = "https://github.com/somenzz/dbinterface"
PACKAGES = find_packages(exclude=["tests", "tests.*"])

INSTALL_REQUIRES = [
    "pymysql",
    "psycopg2-binary",
    "ibm-db==3.0.4"
]
TEST_SUITE = "tests"
TESTS_REQUIRE = []

CLASSIFIERS = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3.6",
    "Topic :: Software Development",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
]

LONG_DESCRIPTION = readme


params = {
    "name": NAME,
    "version": VERSION,
    "description": DESCRIPTION,
    "keywords": KEYWORDS,
    "author": AUTHOR,
    "author_email": AUTHOR_EMAIL,
    "url": URL,
    "license": LICENSE.read_text(),
    "packages": PACKAGES,
    "install_requires": INSTALL_REQUIRES,
    "tests_require": TESTS_REQUIRE,
    "test_suite": TEST_SUITE,
    "classifiers": CLASSIFIERS,
    "long_description": README.read_text(),
}

if __name__ == "__main__":
    setup(**params, long_description_content_type="text/markdown")
