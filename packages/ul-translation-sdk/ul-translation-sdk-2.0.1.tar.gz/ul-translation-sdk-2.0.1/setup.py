from os import path
from setuptools import setup, find_packages

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='ul-translation-sdk',
    version='2.0.1',
    description='Translation service SDK',
    author='Unic-lab',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['translation_sdk*']),
    include_package_data=True,
    package_data={
        '': ['*.yml', 'py.typed', '*.html'],
        'translation_sdk': ['py.typed', '*.html'],
    },
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent",
    ],
    platforms='any',
    install_requires=[
        # 'ul-api-utils==8.1.4',
        # 'ul-py-tool==2.1.2',
        # 'ul-db-utils==4.0.2',
    ],
)
