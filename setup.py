from setuptools import setup, find_packages

from opensips import version

setup(
    name="opensips",
    version=version.__version__,
    packages=find_packages(),
    install_requires=[],
    author="Darius Stefan",
    author_email="darius.stefan@opensips.org",
    description="OpenSIPS Python Packages",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/OpenSIPS/python-opensips",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    scripts=['scripts/opensips-mi'],
    python_requires=">=3.6"
)
