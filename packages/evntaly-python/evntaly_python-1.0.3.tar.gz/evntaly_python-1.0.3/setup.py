from setuptools import setup, find_packages
import os

this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")

with open(readme_path, "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="evntaly-python",
    version="1.0.3",
    packages=find_packages(),
    install_requires=["requests"],
    description="A Python SDK for Evntaly event tracking platform",
    author="Alameer Ashraf",
    author_email="alameer@evntaly.com",
    url="https://github.com/Evntaly/evntaly-python",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)