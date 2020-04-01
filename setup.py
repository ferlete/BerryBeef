# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    license = f.read()

setup(
    name='BERRYBEEF',
    version='0.1',
    description='Softbeef for Raspberry ..',
    long_description=readme,
    author='Valter Ferlete',
    author_email='ferlete@gmail.com',
    url='https://github.com/ferlete/BERRYBEEF',
    license=license,
    #packages=find_packages(exclude=('tests', 'docs'))
    packages=['BEEF'],
    #install_requires=['array-split==0.5.0',
    #      'markdown'
     # ],
    zip_safe=False, install_requires=['nipals'])
