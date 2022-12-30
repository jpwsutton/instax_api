from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="instax_api",
    version="0.8.0",
    description="Fujifilm Instax SP2 & SP3 Library and CLI Utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jpwsutton/instax_api",
    author="James Sutton",
    author_email="james@jsutton.co.uk",
    license="MIT",
    keywords="instax",
    packages=["instax"],
    install_requires=[
        "Pillow",
    ],
)
