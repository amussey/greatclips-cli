"""Setup configuration for Great Clips CLI."""

from setuptools import setup, find_packages

setup(
    name="greatclips-cli",
    version="0.1.0",
    description="Command line tool for the Great Clips API",
    author="Andrew",
    packages=find_packages(),
    install_requires=[
        "click>=8.0.0",
        "python-dotenv>=0.19.0",
    ],
    entry_points={
        "console_scripts": [
            "greatclips-cli=greatclips.cli:cli",
        ],
    },
    python_requires=">=3.8",
)
