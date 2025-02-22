# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-logging-loki-v2",
    version="0.4.4",
    description="Python logging handler for Grafana Loki, with support to headers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    author="Roman Rapoport",
    author_email="cryos10@gmail.com",
    url="https://github.com/RomanR-dev/python-logging-loki",
    packages=setuptools.find_packages(exclude=("tests",)),
    python_requires=">=3.6",
    install_requires=["rfc3339>=6.1", "requests"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Logging",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
