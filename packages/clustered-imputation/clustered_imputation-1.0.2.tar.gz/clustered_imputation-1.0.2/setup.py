from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.2'
DESCRIPTION = 'Adding correlation to handle MNAR'
LONG_DESCRIPTION = 'A package that allows us to impute for all types of missingness(MAR , MCAR , MNAR)'

# Setting up
setup(
    name="clustered_imputation",
    version=VERSION,
    author="MRINAL KANGSA BANIK",
    author_email="<manukbanik30@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['numpy' ,'pandas' , "scikit-learn",'fancyimpute'],
    keywords=['python', 'imputation', 'MNAR'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)