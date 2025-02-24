#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.md") as readme_fh:
    readme = readme_fh.read()

with open("docs/CHANGELOG.md") as changelog_fh:
    changelog = changelog_fh.read()

requirements = ["Click>=7.0", "PyYAML", "Rich"]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email="jai.python3@gmail.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="A lightweight REST API implemented using FastAPI for providing read-only endpoints for the controlled vocabulary implemented in the controlled-vocabulary-utils.",
    entry_points={
        "console_scripts": [
            "run-queries=controlled_vocabulary_fastapi.run_queries:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="controlled_vocabulary_fastapi",
    name="controlled_vocabulary_fastapi",
    packages=find_packages(
        include=["controlled_vocabulary_fastapi", "controlled_vocabulary_fastapi.*"]
    ),
    package_data={
        "controlled_vocabulary_fastapi": [
            "conf/config.yaml",
        ]
    },
    # scripts=["scripts/make_executables_and_aliases.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/controlled-vocabulary-fastapi",
    version="0.1.0",
    zip_safe=False,
)
