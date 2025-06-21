
from setuptools import setup, find_packages

setup(
    name="cdktf-google-vpc", # This is the package name you'll import
    version="0.1.0", # IMPORTANT: Version your module!
    packages=find_packages(), # This will find 'cdktf-google-vpc'
    install_requires=[
        "cdktf>=0.21.0", # Pin to a compatible CDKTF version
        "constructs>=10.4.2",
        "cdktf-cdktf-provider-google>=16.2.0", # Match your Google provider version!
    ],
    author="Anoop Kumar",
    author_email="cdktfbuilder@gmail.com",
    description="A reusable CDKTF Google Cloud VPC module",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/anoopdevopseng/cdktf-google-vpc", # Your repo URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License", # Or MIT, etc.
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)