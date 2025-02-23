import json
from setuptools import setup, find_packages

DESCRIPTION = 'A package with gRPC generated code'
LONG_DESCRIPTION = 'A package with gRPC generated code of the tarot services'

version = json.load(open('package.json'))['version']

# Setting up
setup(
    name="tarot_contracts",
    version=version,
    author="Vlad Balabash",
    author_email="<vladb951@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    package_data={
        '': ['*.pyi']
    },
    install_requires=[],
    keywords=['python', 'grpc', 'tarotbot'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
