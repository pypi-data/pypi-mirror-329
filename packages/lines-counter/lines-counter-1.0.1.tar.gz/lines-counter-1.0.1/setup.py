from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

setup(
    name="lines-counter",
    author="LineCounters - UADY",
    description="A logical & physical lines counter for Python files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    version="1.0.1",
    packages=find_packages(),
    url="https://github.com/LineCounters/LinesCounter",
)
