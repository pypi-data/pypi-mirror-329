import os
from setuptools import setup, find_packages

version = os.getenv('PACKAGE_VERSION', '0.0.1')

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='milgeo',
    version=version,
    description='Common geometries for mil applications',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown',
    author='Adam Wood',
    author_email='adamwoodintel@gmail.com',
    url='https://github.com/adamwoodintel/milgeo',
    packages=find_packages(),
    classifiers=[],
    python_requires='>=3.11',
    install_requires=required,
    include_package_data=True,
    package_data={
        'milgeo': ['kropyva/mapping.csv']
    }
)
