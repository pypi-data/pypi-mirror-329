# prompt: create files for a pip pypi package called boxly, a shapely alternative for bounding boxes. Also create a readme. Prefix each file with a comment line of the filename, create at least a setup.py and a README.md

# setup.py
from setuptools import setup, find_packages

setup(
    name='ancientgreek',
    version='0.2.1',
    packages=find_packages(),
    install_requires=["stanza>=1.2", "Levenshtein", "huggingface_hub>0.29.1"],
    author='Silvia Stopponi, Jasper K. Bos',
    author_email='',
    description="AGILe, Ancient Greek Inscriptions Lemmatizer",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/agile-gronlp/agile/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Or your chosen license
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.0',
)