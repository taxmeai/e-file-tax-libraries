# irs-forms/setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="irs-forms",
    version="1.0.0",
    author="Ope Olatunji",
    author_email="ope.olatunji@taxmeai.com",
    description="Official IRS Forms Processing and E-Filing Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taxmeai/e-file-tax-libraries/irs-forms",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "lxml>=4.6.0",
        "reportlab>=3.5.0",
        "PyPDF2>=2.0.0",
        "pillow>=8.0.0",
        "python-dateutil>=2.8.0",
        "cryptography>=3.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
        "pdf": [
            "pdftk-java>=3.0.0",
        ],
    },
    package_data={
        "irs_forms": [
            "data/*.json",
            "data/forms/*.json",
            "data/schemas/*.xsd",
            "templates/*.xml",
        ],
    },
    entry_points={
        "console_scripts": [
            "irs-forms=irs_forms.cli:main",
            "update-forms=irs_forms.updater:main",
        ],
    },
)
