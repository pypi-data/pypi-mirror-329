from setuptools import setup, find_packages
import os

# Read the contents of README file
with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
    long_description = f.read()

setup(
    name="geodb-finder",
    version="0.2.1",
    author="Gert-jan Poortman",
    author_email="info@esocoding.dev",
    description="A timezone and geolocation database finder.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.esocoding.dev",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'geodb_finder': ['data/*.db'],
    },
    install_requires=[
        'aiosqlite>=0.21.0',
    ],
    extras_require={
        'dev': [
            'pytest>=8.3.4',
            'wheel>=0.45.1',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
