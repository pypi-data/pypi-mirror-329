# Preparing imports.
from setuptools import setup, find_packages
import codecs
import os

# Prepare project details.
VERSION = '1.0.3'
DESCRIPTION = 'Minimalistic Machine Learning Toolset.'
LONG_DESCRIPTION = ('A package that allows for rapid training and usage of various models. '
                    'One click for training, one click for prediction.'
                    )

# Obtain read-me details for long description.
current_location = os.path.abspath(os.path.dirname(__file__))
with codecs.open(os.path.join(current_location, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

# Setting up package details.
setup(
    name="RapidUseML",
    version=VERSION,
    author="5krus (Eryk Krusinski)",
    author_email="<eryk@krus.co.uk>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['pandas', 'joblib', 'numpy', 'scipy', 'scikit-learn'],
    keywords=[
        'machine learning',
        'whittle laboratory'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)