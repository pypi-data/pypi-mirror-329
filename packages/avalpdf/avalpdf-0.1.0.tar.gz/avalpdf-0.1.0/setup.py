from setuptools import setup, find_packages

setup(
    name='avalpdf',
    version='0.1.0',
    author="Dennis Angemi",
    author_email="dennisangemi@gmail.com",
    url="https://github.com/dennisangemi/avalpdf",
    packages=find_packages(),
    install_requires=[
        'pdfix-sdk'
    ],
    entry_points={
        'console_scripts': [
            'avalpdf = avalpdf.cli:main',
        ],
    },
)