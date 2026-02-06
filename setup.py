"""
Setup configuration for upd-builder package
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="upd-builder",
    version="1.0.2",
    author="Georgy",
    author_email="givi.zirabuch@gmail.com",
    description="Генератор валидного УПД (Универсального Передаточного Документа) в формате XML файла в соответствии со спецификацей XSD v5.03",
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/daoman/upd-builder",
    project_urls={
        "Bug Tracker": "https://github.com/daoman/upd-builder/issues",
        "Documentation": "https://github.com/daoman/upd-builder/docs",
        "Source Code": "https://github.com/daoman/upd-builder",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: Russian",
    ],
    python_requires=">=3.9",
    install_requires=[
        # No required dependencies - uses only Python stdlib
    ],
    extras_require={
        "yaml": ["ruamel.yaml>=0.17.0"],
        "validation": ["xmlschema>=2.0.0"],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=0.990",
            "ruamel.yaml>=0.17.0",
            "xmlschema>=2.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
    keywords=[
        "upd",
        "xml",
        "diadoc",
        "transfer document",
        "счет-фактура",
        "Универсальный Передаточный Документ",
        "УПД",
    ],
)
