"""
ARXML Parser and Editor Tool
--------------------------
A Python tool for parsing and editing AUTOSAR XML (ARXML) files.
Features:
- Parse ARXML files and display their structure
- View and modify software components
- Update parameter values
- Add new components
- Merge multiple ARXML files
"""

from setuptools import setup, find_packages

setup(
    name="arxml-tool",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "autosar>=0.3.2",
        "lxml>=4.9.0",
        "click>=8.0.0",
        "requests>=2.28.0",  # For schema downloads
    ],
    entry_points={
        "console_scripts": [
            "arxml=src.main:cli",
        ],
    },
    python_requires=">=3.6",
    author="Adarsh",
    author_email="jk.adarsh.2002@gmail.com",
    description="A tool for parsing and editing AUTOSAR XML (ARXML) files",
    long_description=__doc__,
    keywords="autosar, arxml, automotive, xml, parser, editor",
    url="https://github.com/adarshjagadishkamini/autosar_arxml-parser_editor.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
        "Topic :: Text Processing :: Markup :: XML",
    ],
)