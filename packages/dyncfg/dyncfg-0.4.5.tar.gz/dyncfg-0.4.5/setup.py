from setuptools import setup, find_packages


from pathlib import Path

# Get the directory where the current file (setup.py) is located
this_directory = Path(__file__).parent

long_description = (this_directory / "readme.md").read_text(encoding="utf-8")


setup(
    name="dyncfg",
    version="0.4.5",
    author="Lukas G. Olson",
    author_email="olson@student.ubc.ca",
    description="A dynamic, easy-to-use .ini configuration system built for humans.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lukasgolson/dyncfg",
    packages=find_packages(),  # Automatically discover all packages and subpackages
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
