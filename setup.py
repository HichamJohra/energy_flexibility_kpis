import os
import re
import setuptools

# define constants
PACKAGE_NAME = "energy_flexibility_kpis"
GITHUB_ACCOUNT = "HichamJohra"
AUTHOR_NAME = "Hicham Johra"
AUTHOR_EMAIL = "hj@build.aau.dk"
REPOSITORY_NAME = PACKAGE_NAME
ROOT_PATH = os.path.dirname(__file__) # repository root path
# require at least python version 3.7 to use the package. 
# Higher version requirements might be exclusive 
# and require user to update legacy systems with newer python distributions.
MINIMUM_PYTHON_VERSION = '3.7'

# use README.md as long descirption
with open('README.md', 'r') as fh:
    long_description = fh.read()

# parse the requirement file and remove invalid text like comments and white space
with open('requirements.txt', 'r') as fh:
   requirements = fh.readlines()
   requirements = [requirement.strip().replace('\n','').replace('\r','') for requirement in requirements]
   requirements = [requirement for requirement in requirements if len(requirement) != 0 and requirement[0] != '#']

# read the version from __init__.py
def get_version():
    init = open(os.path.join(ROOT_PATH, PACKAGE_NAME, "__init__.py")).read()
    return re.compile(r'''__version__ = ['"]([0-9.]+)['"]''').search(init).group(1)

setuptools.setup(
    version=get_version(),
    name=PACKAGE_NAME,  # Name of the package
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="Python package for the computation of energy flexibility KPIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url=f"https://github.com/{GITHUB_ACCOUNT}/{PACKAGE_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{GITHUB_ACCOUNT}/{REPOSITORY_NAME}/issues",
        "Documentation": f"https://github.com/{GITHUB_ACCOUNT}/{REPOSITORY_NAME}",
        "Source Code": f"https://github.com/{GITHUB_ACCOUNT}/{REPOSITORY_NAME}",
    },
    packages=setuptools.find_packages(),
    python_requires=f">={MINIMUM_PYTHON_VERSION}",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,  # Automatically install the requirements
)
