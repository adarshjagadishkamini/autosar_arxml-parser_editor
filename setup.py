from setuptools import setup, find_packages

setup(
    name="arxml-tool",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "autosar",
        "lxml",
        "click",
    ],
    entry_points={
        "console_scripts": [
            "arxml=src.main:cli",
        ],
    },
    python_requires=">=3.6",
    author="Your Name",
    author_email="your.email@example.com",
    description="A tool for parsing and editing AUTOSAR XML (ARXML) files",
    keywords="autosar, arxml, automotive",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)