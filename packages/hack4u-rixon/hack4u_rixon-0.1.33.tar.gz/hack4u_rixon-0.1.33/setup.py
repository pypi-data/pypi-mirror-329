#!/usr/bin/env python3

from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_rixon",
    version="0.1.33",
    packages=find_packages(),
    install_requires=[],
    author="Rixon huaman",
    description="Una biblioteca para consultar los cursos de hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io",
)
