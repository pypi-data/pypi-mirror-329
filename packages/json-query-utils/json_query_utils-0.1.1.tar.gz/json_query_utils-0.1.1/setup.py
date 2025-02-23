#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "PyYAML", "Rich", "jsonpath_ng"]

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
    description="Collection of Python scripts to run queries on a JSON file.",
    entry_points={
        "console_scripts": [
            "json-query-utils-query-file=json_query_utils.query_json_file:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="json_query_utils",
    name="json_query_utils",
    packages=find_packages(include=["json_query_utils", "json_query_utils.*"]),
    package_data={
        "json_query_utils": [
            "conf/config.yaml",
        ]
    },
    # scripts=["scripts/make_executables_and_aliases.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/json-query-utils",
    version="0.1.1",
    zip_safe=False,
)
