from setuptools import setup, find_packages

setup(
    name='pytrace',
    version='0.0.1',
    description='An strace-like tool for Python audit events',
    packages=find_packages(),
    python_requires='>=3.8',
    entry_points={
        'console_scripts': [
            'pytrace = pytrace.__main__:main',
        ]
    }
)
