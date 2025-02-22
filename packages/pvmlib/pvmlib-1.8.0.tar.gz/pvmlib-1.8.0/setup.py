from setuptools import setup, find_packages
from pvmlib.info_lib import LibraryInfo

setup(
    name=LibraryInfo.name,
    version=LibraryInfo.version_lib.lstrip("v"),
    packages=find_packages(),
    install_requires=LibraryInfo.install_requires,
    author=LibraryInfo.author,
    author_email=LibraryInfo.author_email,
    description=LibraryInfo.description,
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    zip_safe=False,
    python_requires=LibraryInfo.python_requires,
)