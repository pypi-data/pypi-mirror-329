from setuptools import setup, find_packages
import os

def read(*paths):
    with open(os.path.join(*paths), 'r') as f:
        return f.read()

requirements = [
    "jellyfish",
    "regex",
]

setup(
    name="autocorrect_kh",
    version="0.3.1",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'autocorrect_kh': [
            'data/phum/*.txt',
            'data/khum/*.txt',
            'data/*.txt'
        ],
    },
    install_requires=[
        "jellyfish",
        "regex",
    ],
    author="Kim Ouddommony",
    author_email="kimmony039@gmail.com",
    description="An autocorrect Khmer Address and Specifically for Khmer National ID Card",
    long_description=(read('README.md')),
    long_description_content_type='text/markdown',
    url="https://github.com/monykappa/autocorrect-kh.git",
)
