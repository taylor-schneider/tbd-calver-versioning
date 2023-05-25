import sys
import setuptools
import tbd_calver_versioning
import logging
import sys


logging.basicConfig(level=logging.DEBUG, filename="/tmp/foobar.log")

logging.debug("=====================")
logging.debug(sys.path)
logging.debug(sys.executable)
logging.debug("=====================")

install_requires = [
    "tbd-calver-versioning"
]

if sys.version_info < (3, 0):
    install_requires.append("future")

source_code_dir = "src"

setuptools.setup(
    name="DummyPackage",
    version=tbd_calver_versioning.determine_version_number(),
    author="tschneider",
    author_email="my@email.com",
    description="A dummy package for testing purposes.",
    long_description="This is a longer description filled with more information.",
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(source_code_dir),
    package_dir={
        "": source_code_dir
    },
    install_requires= install_requires,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "LICENSE :: OSI APPROVED :: GNU GENERAL PUBLIC LICENSE V3 (GPLV3)",
        "Operating System :: OS Independent",
    ],
)