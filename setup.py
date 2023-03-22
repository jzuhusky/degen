from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

version = (this_directory / "__version__.txt").read_text()

setup(
    name="degen",
    version=version,
    description="Programming with betting odds, made simple",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Joey Zuhusky",
    keywords="odds sportsbetting betting python betting gambling",
    author_email="jzuhusky@gmail.com",
    maintainer_email="jzuhusky@gmail.com",
    url="https://github.com/jzuhusky/degen",
    install_requires=["pydantic>=1.10.6"],
    license="MIT",
    packages=["degen"],
)
