from setuptools import setup
from setuptools import find_packages

VERSION = '0.2.3'

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = [l for l in f.read().splitlines() if l]

setup(
    name='InsCode',  # package name
    version=VERSION,  # package version
    description='Inscode SDK',  # package description
    long_description=long_description,  # 长简介 这里使用的 readme 内容
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False,
    python_requires='>=3'
)
