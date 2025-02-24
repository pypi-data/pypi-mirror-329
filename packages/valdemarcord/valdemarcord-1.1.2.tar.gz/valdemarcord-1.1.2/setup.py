from setuptools import setup, find_packages

setup(
    name="valdemarcord",
    version="1.1.2",
    packages=find_packages(),
    description="discord api wrapper (beta)",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    
    author="valdemarkid",
    install_requires=[
        'requests',
        'beautifulsoup4',
        'orjson',
        'websocket-client'
    ],
    python_requires=">=3.6",
)