from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='FlexfillsApi',
    version='0.2.0',
    packages=find_packages(),
    install_requires=required,
    author='Djordje Nikolic',
    author_email="magic.guru88@gmail.com",
    description="This package is for using Flex Fills WebSocket communication with FlexFills trading services.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Flexfills-UI/Hermes',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
