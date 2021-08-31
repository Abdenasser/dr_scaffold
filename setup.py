from setuptools import find_packages, setup

with open("README.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "dr_scaffold"
VERSION = "v2.0.0"
DESCRIPTION = "a Django package for scaffolding django rest apis using cli"
LONG_DESCRIPTION = (long_description,)
URL = "https://github.com/Abdenasser/dr_scaffold"
AUTHOR = "abdenasser"
AUTHOR_EMAIL = "nasser.elidrissi065@gmail.com"
LICENSE = "MIT"
PACKAGES = [
    "dr_scaffold",
    "dr_scaffold.scaffold_templates",
    "dr_scaffold.management",
    "dr_scaffold.management.commands",
]
REQUIREMENTS = ["django", "inflect"]
CLASSIFIERS = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Web Environment",
    "Framework :: Django",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]

EXCLUDE_FROM_PACKAGES = []

setup(
    name=NAME,
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
    zip_safe=False,
)
