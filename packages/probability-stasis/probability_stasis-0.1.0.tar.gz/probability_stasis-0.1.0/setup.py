from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="probability_stasis",
    version="0.1.0",
    author="Crispine Mwangi Wachira",
    author_email="author@example.com",
    description="A Python library for filtering and stabilizing probability predictions from multiple models inspired by Rick and Morty",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chrispin-m/probability_stasis",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
