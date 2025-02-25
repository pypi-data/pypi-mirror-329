from setuptools import setup, find_packages

setup(
    name="finmetrics",
    version="0.1.3",
    author="Mihir Gajjar",
    description="A python package to perform financial operations",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/MihirGajjar27/finmetrics",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9.6',
    license_files=[],
)
