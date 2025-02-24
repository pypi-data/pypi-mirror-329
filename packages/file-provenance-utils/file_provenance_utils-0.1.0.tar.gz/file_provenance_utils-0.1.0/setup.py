#!/usr/bin/env python
"""The setup script."""
import os
from setuptools import setup, find_packages

with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme_fh:
    readme = readme_fh.read()

with open("HISTORY.rst") as changelog_fh:
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
    description="Collection of functions for inserting provenance information to the output files.",
    entry_points={
        "console_scripts": [
            "run-queries=file_provenance_utils.run_queries:main",
        ],
    },
    install_requires=requirements,
    long_description=readme + "\n\n" + changelog,
    long_description_content_type="text/markdown",
    include_package_data=True,
    keywords="file_provenance_utils",
    name="file_provenance_utils",
    packages=find_packages(
        include=["file_provenance_utils", "file_provenance_utils.*"]
    ),
    package_data={
        "file_provenance_utils": [
            "conf/config.yaml",
        ]
    },
    # scripts=["scripts/make_executables_and_aliases.py"],
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/jai-python3/file-provenance-utils",
    version="0.1.0",
    zip_safe=False,
)
