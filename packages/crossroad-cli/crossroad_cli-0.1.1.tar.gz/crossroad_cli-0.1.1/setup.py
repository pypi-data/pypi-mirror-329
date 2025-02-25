from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crossroad-cli",  # This is the PyPI package name
    version="0.1.1",
    packages=find_packages(),  # This will automatically find all packages
    package_data={
        'crossroad': ['**/*'],  # Include all files in the crossroad directory
    },
    include_package_data=True,  # Include other non-Python files
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-multipart",
        "pandas",
        "pydantic",
        "requests"
    ],
    entry_points={
        "console_scripts": [
            "crossroad=crossroad.cli.main:main",
        ],
    },
    author="Pranjal Pruthi, Preeti Agarwal",
    author_email="your.email@igib.res.in",  # Add your institutional email
    description="A tool for analyzing SSRs in genomic data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pranjalpruthi/crossroad",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Development Status :: 4 - Beta",
    ],
    python_requires=">=3.8",
    # External tool dependencies
    extras_require={
        'external': [
            'seqkit',
            'seqtk',
            'bedtools'
        ]
    }
)