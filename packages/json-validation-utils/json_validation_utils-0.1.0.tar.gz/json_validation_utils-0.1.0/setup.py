#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements = ["Click>=7.0", "PyYAML", "Rich", "genson", "jsonschema"]

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
    description="Collection of Python scripts for generating a JSON schema and performing JSON schema validation.",
    entry_points={
        "console_scripts": [
            "json-validation-utils-generate-json-schema=json_validation_utils.generate_json_schema:main",
            "json-validation-utils-validate-json-file=json_validation_utils.validate_json_file:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="json_validation_utils",
    name="json_validation_utils",
    packages=find_packages(
        include=["json_validation_utils", "json_validation_utils.*"]
    ),
    package_data={
        "json_validation_utils": [
            "conf/config.yaml",
        ]
    },
    # scripts=["scripts/make_executables_and_aliases.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/json-validation-utils",
    version="0.1.0",
    zip_safe=False,
)
