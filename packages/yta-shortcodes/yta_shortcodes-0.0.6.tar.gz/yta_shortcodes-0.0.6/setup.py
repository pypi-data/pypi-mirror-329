from setuptools import setup, find_packages


VERSION = '0.0.6'
DESCRIPTION = 'Youtube Autonomous Shortcodes Module.'
LONG_DESCRIPTION = 'This is the Youtube Autonomous Shortcodes module'

setup(
    name = "yta_shortcodes", 
    version = VERSION,
    author = "Daniel Alcalá",
    author_email = "<danielalcalavalera@gmail.com>",
    description = DESCRIPTION,
    long_description = LONG_DESCRIPTION,
    packages = find_packages(),
    install_requires = [
        'yta_general_utils',
        'shortcodes',
    ],
    
    keywords = [
        'youtube autonomous shortcodes module software'
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