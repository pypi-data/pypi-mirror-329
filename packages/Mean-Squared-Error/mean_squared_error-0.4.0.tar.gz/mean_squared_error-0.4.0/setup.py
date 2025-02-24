from setuptools import setup, find_packages

with open("README.md") as file:
    description=file.read()
setup(
    name="Mean_Squared_Error",
    version="0.4.0",
    packages=find_packages(),
    install_requires=[
# add dependencies (if applicable)
    ],
    long_description=description,
    long_description_content_type="text/markdown",
)