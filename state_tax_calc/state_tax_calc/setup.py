# state-tax-calc/setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="state-tax-calc",
    version="0.1.0",
    author="Ope Olatunji",
    author_email="ope.olatunji@taxmeai.com",
    description="US State Tax Calculation Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/taxmeai/e-file-tax-libraries/state-tax-calc",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
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
        "python-tax>=0.1.0",
        "requests>=2.25.0",
        "lxml>=4.6.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
        ],
    },
    package_data={
        "state_tax_calc": [
            "data/states/*.json",
            "data/rates/*.json",
            "data/forms/*.json",
        ],
    },
    entry_points={
        "console_scripts": [
            "state-tax-calc=state_tax_calc.cli:main",
        ],
    },
)
