from setuptools import setup, find_packages

setup(
    name='snaketrace',
    version='0.0.1',
    description='An strace-like tool for Python audit events',
    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'snaketrace = snaketrace.__main__:main',
        ]
    }
)
