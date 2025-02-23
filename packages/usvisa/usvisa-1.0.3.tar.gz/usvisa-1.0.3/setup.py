import os
from setuptools import find_packages, setup

#Metadata of package

NAME = 'usvisa'
DESCRIPTION = 'Usvisa_prediction_model'
EMAIL = 'ashfaq664236@gmail.com'
AUTHOR = 'ashpaqueshaikh4236'
REQUIRES_PYTHON = '==3.8.20'

pwd = os.path.abspath(os.path.dirname(__file__))


#get the list of packages to be installed
HYPEN_E_DOT='-e .'
def get_requirements(file_path):
    '''
    this function will return the list of requirements
    '''
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("\n","") for req in requirements]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    
    return requirements
    
# Read the README file
try:
    with open(os.path.join(pwd, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

#Load the packages's version 
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
PACKAGE_DIR = os.path.join(ROOT_DIR, NAME)



about = {}
try:
    with open(os.path.join(PACKAGE_DIR, 'VERSION')) as f:
        about['__version__'] = f.read().strip()
except FileNotFoundError:
    raise RuntimeError("VERSION file not found. Ensure it exists in the package directory.")


setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    packages=find_packages(),
    package_data={'Usvisa_prediction_model': ['VERSION']},
    install_requires=get_requirements('requirements.txt'),
    extras_require={},
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)