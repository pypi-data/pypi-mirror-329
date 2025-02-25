from os import path

from setuptools import setup, find_packages

with open(path.join(path.abspath(path.dirname(__file__)), "README.md"), 'r', encoding="utf-8") as f:
    long_description = f.read()

setup(
    # https://packaging.python.org/specifications/core-metadata/#name
    name="basking-sdk",  # Required
    # https://www.python.org/dev/peps/pep-0440/
    version="{VERSION}",
    description="Basking.io python SDK",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://basking.io",
    author="Basking Automation GmbH",
    author_email="info@basking.io",
    keywords="occupancy analytics data api bas basking basking.io",
    packages=find_packages(where="./src/",exclude=["tests*"]),
    package_dir={"basking": "./src/basking"},
    python_requires=">=3.7, <4",
    install_requires=[
        "backoff>=2.0.0",
        "boto3>=1.0.0",
        "botocore>=1.0.0",
        "certifi",
        "charset-normalizer",
        "graphqlclient>=0.2.0",
        "idna",
        "jmespath",
        "numpy",
        "pandas>=1.0.0",
        "python-dateutil>=2.0.0",
        "pytz",
        "requests>=2.0.0",
        "s3transfer",
        "six",
        "urllib3",
    ],
    project_urls={
        "Bug Reports": "https://basking.io/contact-us/",
        "Official Website": "https://www.basking.io",
        "Platform Access": "https://app.basking.io"
    },
)
