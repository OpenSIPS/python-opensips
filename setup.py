from setuptools import setup, find_packages

setup(
    name="opensips",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    author="Darius Stefan",
    author_email="darius.stefan@opensips.org",
    description="OpenSIPS Python Package for MI and Event Interface",
    url="https://github.com/OpenSIPS/python-opensips",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6"
)