import os
from setuptools import setup, find_packages

# Get the absolute path of the current directory
this_directory = os.path.abspath(os.path.dirname(__file__))
readme_path = os.path.join(this_directory, "README.md")

# Ensure README.md exists before reading it
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "A Python SDK for Evntaly event tracking and analytics."

setup(
    name="evntaly-python",
    version="1.0.5",
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