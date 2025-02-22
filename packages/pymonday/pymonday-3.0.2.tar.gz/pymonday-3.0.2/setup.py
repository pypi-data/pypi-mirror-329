from setuptools import setup, find_packages

# Read the contents of README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='pymonday',
    version='3.0.2',
    packages=find_packages(include=['pymonday', 'pymonday.*']),
    include_package_data=True,
    description='pyMonday is a monday.com API Python Client Library, compatible with API version 2025-01 and later.',
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires=['httpx', 'python-dotenv', 'PyYAML', 'asyncio'],
)