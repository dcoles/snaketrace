import os
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='snaketrace',
    version='0.2.0',
    description='An strace-like tool for Python audit events',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dcoles/snaketrace',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'snaketrace = snaketrace.__main__:main',
        ] + ([
            '\N{SNAKE}trace = snaketrace.__main__:main',
        ] if os.getenv('ANTIGRAVITY') else []),
    },
)
