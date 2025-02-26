# Created by A. MATHIEU at 25/02/2025
from setuptools import setup, find_packages

# with open('requirements.txt') as f:
#     required = f.read().splitlines()

setup(
    name='pv_ivcurve',
    version='1.0',
    packages=find_packages(),
    description='IV-curve package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Alexandre MATHIEU',
    author_email='mathalex@gmail.com',
    url='https://github.com/AlexandreHugoMathieu/pv_ivcurve',
    python_requires='>=3.9',
    install_requires=[],
)