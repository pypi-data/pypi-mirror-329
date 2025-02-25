"""
Cometa Git Tools - A collection of Git utilities for Commitizen and PR Summary Generation
"""

import os
import re
from setuptools import setup, find_packages


def get_version():
    """Read version from version.py without importing the module."""
    version_file = os.path.join("src", "cz_ai_conventional", "version.py")
    with open(version_file, "r", encoding="utf-8") as f:
        contents = f.read()
    version_match = re.search(r'VERSION\s*=\s*["\']([^"\']+)["\']', contents)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), "README.md"), encoding="utf-8") as f:
    long_description = f.read()


# Read requirements from requirements.txt if it exists
def read_requirements(filename="requirements.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return [
                line.strip() for line in f if line.strip() and not line.startswith("#")
            ]
    except FileNotFoundError:
        return [
            "commitizen>=3.12.0",
            "typer>=0.9.0",
            "rich>=13.7.0",
            "google-generativeai>=0.3.2",
            "absl-py>=2.0.0",
            "questionary>=2.0.1",
        ]


setup(
    name="giji",
    version=get_version(),
    description="Git tools for Commitizen and PR Summary Generation using AI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Cometa",
    author_email="apps@getcometa.com",
    url="https://github.com/cometa/giji",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "typer>=0.9.0",
        "rich>=13.7.0",
        "jira>=3.5.1",
        "google-generativeai>=0.3.2",
        "questionary>=2.0.1",
    ],
    entry_points={
        "console_scripts": [
            "giji=src.cli:main",
        ],
    },
    options={"commitizen": {"name": "cz_ai_conventional"}},
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="git commitizen pr-summary ai gemini conventional-commits",
    project_urls={
        "Bug Reports": "https://github.com/cometa/giji/issues",
        "Source": "https://github.com/cometa/giji",
    },
    package_data={
        "": ["pyproject.toml"],
    },
    data_files=[
        ("", ["pyproject.toml"]),
    ],
)
