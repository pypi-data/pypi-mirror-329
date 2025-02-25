from setuptools import setup, find_packages

setup(
    name="cinnavo",
    version="0.1.0",
    description="Python client for interacting with the Cinnavo API",
    author="Nitya Singh",
    author_email="nitya@cinnavo.com",
    url="https://github.com/yourusername/cinnavo",  # update with your repository
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
