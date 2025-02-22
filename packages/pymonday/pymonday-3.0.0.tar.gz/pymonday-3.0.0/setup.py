from setuptools import setup, find_packages

setup(
    name='pymonday',
    version='3.0.0',
    packages=find_packages(include=['pymonday', 'pymonday.*']),
    include_package_data=True,
    install_requires=['httpx', 'python-dotenv', 'PyYAML', 'asyncio'],
)