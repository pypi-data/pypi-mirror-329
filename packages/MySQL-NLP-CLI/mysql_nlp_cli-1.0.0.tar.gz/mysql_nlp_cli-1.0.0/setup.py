from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.0'
DESCRIPTION = 'A Python package that allows to use the CLI and Natural Language processing to write MySQL queries.'
LONG_DESCRIPTION = 'A Python package that allows to use the Command Line Interface and Natural Language Processing to write MySQL queries. Alternatively, uses CLI inputs to generate specific code.'

# Setting up
setup(
    name="MySQL_NLP_CLI",
    version=VERSION,
    author="Kunaal Gadhalay",
    author_email="<kunaalgadhalay93@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['venv', 'argparse', 'logging', 'pathlib', 're' ,'getpass', 'mysql-connector-python', 'spacy', 'download', 'en_core_web_sm' 'typing','dataclasses'],
    keywords=['python', 'cli', 'NLP', 'mysql', 'Command', 'Line', 'Interface', 'Natural', 'Language', 'Processing'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.6',
)