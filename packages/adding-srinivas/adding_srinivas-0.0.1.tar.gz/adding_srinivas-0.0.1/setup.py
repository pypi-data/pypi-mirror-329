from setuptools import setup ,find_packages
import codecs
import os
version="0.0.1"
Description="add number package"

setup(
    name="adding-srinivas",
    version=version,
    author="srinivas",
    description=Description,
    packages=find_packages(),
    install_require=['pandas'],
    keywords=["python","video","videostream"],
    classifiers=[
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows"
]
    
)