from setuptools import find_packages, setup

with open("PYPIREADME.rst", "r", encoding="utf-8") as fh:
    long_description = fh.read()

NAME = "dr_scaffold"
VERSION = "v2.1.2"
DESCRIPTION = "a Django package for scaffolding django rest apis using cli"
LONG_DESCRIPTION = (long_description,)
LONG_DESCRIPTION_CONTENT_TYPE = "text/x-rst"
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
REQUIREMENTS = ["django", "inflect", "isort"]
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
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
]

EXCLUDE_FROM_PACKAGES = []

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
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
