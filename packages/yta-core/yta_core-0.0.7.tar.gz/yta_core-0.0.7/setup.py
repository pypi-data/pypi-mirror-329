from setuptools import setup, find_packages


VERSION = '0.0.7'
DESCRIPTION = 'Youtube Autonomous Core'
LONG_DESCRIPTION = 'Youtube Autonomous Core - where the magic happens.'

setup(
    name = "yta_core", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_general_utils'
    ],
    
    keywords = [
        'youtube autonomous core',
    ],
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)