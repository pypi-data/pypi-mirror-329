from setuptools import setup, find_packages

setup(
    name="dbautomodel",
    version="0.0.1",
    author="Aero",
    author_email="email@example.com",
    description="lib for auto model sql queries",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Myshica/dbautomodel",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.12',
)