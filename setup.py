PACKAGE = "dr_scaffold"
NAME = "dr_scaffold"
DESCRIPTION = "a Django app for scaffolding django rest apis using cli"
AUTHOR = "Nasser El Idrissi"
AUTHOR_EMAIL = "nasser.elidrissi065@gmail.com"
URL = "https://github.com/Abdenasser/drf_scaffold"
VERSION = __import__(PACKAGE).__version__

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.rst"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="MIT",
    url=URL,
    packages=find_packages(exclude=["tests.*", "tests"]),
    package_data=find_package_data(PACKAGE, only_in_packages=False),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
        ],
    install_requires=[
        "Django==3.2.6",
        "django-filter==2.4.0",
        "djangorestframework==3.12.4",
        "inflect==5.3.0",
        "Markdown==3.3.4",
        ],
    zip_safe=False
)
