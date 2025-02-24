from setuptools import setup, find_packages
from os import path

# Read the content of your README.md file
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


VERSION = '0.1.9' 
DESCRIPTION = 'gapSolutions client package'

# Setting up
setup(
       # the name must match the folder name 'gapSolutions_client'
        name="gapSolutions_client", 
        version=VERSION,
        author="Samer Hisham",
        author_email="samerrhisham@gmail.com",
        url="https://bitbucket.org/designoptics/api-python-wrapper/src/master/",
        description=DESCRIPTION,
        long_description=long_description,
        long_description_content_type='text/markdown',
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'

        keywords=['python', 'gapSolutions'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)
