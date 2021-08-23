import codecs
import re
import os

from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def get_version(filename):
    with codecs.open(filename, 'r', 'utf-8') as fp:
        contents = fp.read()
    return re.search(r"__version__ = ['\"]([^'\"]+)['\"]", contents).group(1)

NAME = 'dr_scaffold'
VERSION = get_version(os.path.join('dr_scaffold', '__init__.py'))
DESCRIPTION = 'a Django package for scaffolding django rest apis using cli'
LONG_DESCRIPTION=long_description,
URL = 'https://github.com/Abdenasser/dr_scaffold'
AUTHOR = 'abdenasser'
AUTHOR_EMAIL = 'nasser.elidrissi065@gmail.com'
LICENSE = 'MIT'
PACKAGES=[
        'dr_scaffold',
        'dr_scaffold.scaffold_templates',
        'dr_scaffold.management',
        'dr_scaffold.management.commands']
REQUIREMENTS = ['django','inflect']
CLASSIFIERS=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: System :: Installation/Setup']

EXCLUDE_FROM_PACKAGES = []

setup(name=NAME,
      version=VERSION,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION,
      url=URL,
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
      install_requires=REQUIREMENTS,
      include_package_data=True,
      classifiers=CLASSIFIERS,
      zip_safe=False)