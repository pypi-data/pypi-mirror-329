import os
from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="starmoth",
    version=os.environ.get("MOTH_VERSION"),
    author="Gudjon Magnusson",
    author_email="gmagnusson@fraunhofer.org",
    description="A small wrapper library to help test systems using STAR",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="proprietary",
    packages=["moth", "moth.cli", "moth.server", "moth.message", "moth.driver"],
    keywords="Fraunhofer, STAR, testing",
    python_requires=">=3.7, <4",
    install_requires=["pyzmq>=25.0.0", "numpy>=1.14.5", "msgpack>=1.0.4", "colorlog>=6.0.0"],
    entry_points={
        "console_scripts": [
            "moth=moth.cli:cli",
        ]
    },
)
