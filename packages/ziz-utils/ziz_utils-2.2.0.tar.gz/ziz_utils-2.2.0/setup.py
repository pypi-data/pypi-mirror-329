from setuptools import setup, find_packages

VERSION = "2.2.0"
DESCRIPTION = "A collection of Python function that I used in my projects."
with open("README.md") as file:
    LONG_DESCRIPTION = file.read()

setup(
    name = "ziz_utils",
    version = VERSION,
    author = "Zizel",
    author_email = "danbua999@gmail.com",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    long_description_content_type = "text/markdown",
    url = "https://github.com/uwungu01-rep/ziz_utils",
    packages = find_packages(),
    install_requires = [], 
    classifiers = [
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)