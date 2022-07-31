import os
from distutils.core import setup

with open('requirements.txt') as f:
    required_pkgs = f.read().splitlines()

setup(
    name="degen",
    version="0.1.0",
    description="Programming with betting odds, made simple",
    author="Joey Zuhusky",
    keywords="odds sportsbetting betting python betting gambling",
    author_email="jzuhusky@gmail.com",
    maintainer_email="jzuhusky@gmail.com",
    url="https://github.com/jzuhusky/degen",
    install_requires=required_pkgs,
)
