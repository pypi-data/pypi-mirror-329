import os
import pathlib
from setuptools import setup, find_packages

PROJECT = "french-public-holidays"
NAME = "french_public_holidays"
GITHUB = "tsnaketech"

parent = pathlib.Path(__file__).parent.resolve()
version = (parent / 'VERSION').read_text(encoding='utf-8')
long_description = (parent / 'README.md').read_text(encoding='utf-8')

setup(
    name=NAME,
    version=version,
    description='Get French public holidays from the French government API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/{0}/{1}'.format(GITHUB, PROJECT),
    author='SnakeTech',
    author_email='repo@snaketech.net',
    license='MIT',
    packages=find_packages(),
    package_dir={"sample": "sample"},
    include_package_data=True,
    install_requires=[
        'configparser',
        'httpx',
        'pydantic',
        'python-dotenv',
        'PyYAML'
    ],
    project_urls={
        'Source': 'https://github.com/{0}/{1}'.format(GITHUB, PROJECT),
        'Issues': 'https://github.com/{0}/{1}/issues'.format(GITHUB, PROJECT)
    },
    entry_points={
        "console_scripts": [
            f"{PROJECT}={NAME}.__main__:main",
        ],
    },
    # https://pypi.org/classifiers/
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        "Natural Language :: English",
        "Natural Language :: French",
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
    ],
)