from setuptools import setup, find_packages

setup(
    name="structify-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "structify=structify.cli:main"
        ]
    },
)
