from setuptools import setup, find_packages
from os import path

# Read the content of your README.md file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

VERSION = '0.1.23'  # Increment version to force PyPI update
DESCRIPTION = 'gapSolutions client package'

setup(
    name="gapsolutions_client",  # ✅ Matches your package folder
    version=VERSION,
    author="Samer Hisham",
    author_email="samerrhisham@gmail.com",
    url="https://bitbucket.org/designoptics/api-python-wrapper/src/master/",
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    
    # ✅ Automatically finds and includes all sub-packages
    packages=find_packages(include=['gapSolutions_client', 'gapSolutions_client.*']), 
    include_package_data=True,  # ✅ Ensures additional files are included
    install_requires=[
        "requests",
        "python-dateutil" ,  # ✅ Ensures dependencies are installed
    ],
    
    keywords=['python', 'gapSolutions'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
