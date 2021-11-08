from setuptools import setup

setup(
    name='main',
    version='0.1.0',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'mygrep = searchUtilities:grep_via_grep',
            'myre = searchUtilities:grep_via_re',
        ],
    },
)