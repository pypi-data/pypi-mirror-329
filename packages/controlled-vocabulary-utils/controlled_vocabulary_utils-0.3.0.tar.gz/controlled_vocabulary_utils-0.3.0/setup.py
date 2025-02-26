#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "PyYAML", "Rich", "singleton-decorator"]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email="jai.python3@gmail.com",
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.12",
    ],
    description="A package for evaluating values for terms in a controlled vocabulary.",
    entry_points={
        "console_scripts": [
            "run-queries=controlled_vocabulary_utils.run_queries:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="controlled_vocabulary_utils",
    name="controlled_vocabulary_utils",
    packages=find_packages(
        include=["controlled_vocabulary_utils", "controlled_vocabulary_utils.*"]
    ),
    package_data={
        "controlled_vocabulary_utils": [
            "conf/config.yaml",
        ]
    },
    # scripts=["scripts/make_executables_and_aliases.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/controlled-vocabulary-utils",
    version="0.3.0",
    zip_safe=False,
)
