from setuptools import setup

setup(
    name="salesmanago-toolkit",
    version="0.2.16",
    author="Webparsers",
    author_email="panenotgeor@gmail.com",
    description="Salesmanago Tools is a project designed to simplify working with the Salesmanago API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Web-parsers/SalesmanagoTools",
    packages=[
        'salesmanago_toolkit',
        'salesmanago_toolkit.service',
        'salesmanago_toolkit.utils',
    ],
    install_requires=[
        "aiohttp==3.11.11",
        "requests==2.32.3",
        "pandas<2.2",
        "httpx==0.28.1"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)