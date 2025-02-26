# setup.py

from setuptools import setup, find_packages

setup(
    name="ydapi_sdk",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    author="firework-a",
    author_email="2737459675@qq.com",
    description="A Python SDK for tracking API requests",
    long_description=open("README.md",encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/firework-a/ydapi_sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
)