
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="TgrEzLi",
    version="0.1.1",
    author="eaannist",
    author_email="eaannist@gmail.com",
    description="Easy-to-use synchronous Telegram bot library with async backend and intuitive handlers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eaannist/TgrEzLi",
    packages=find_packages(),
    install_requires=[
        "python-telegram-bot>=20.0",
        "requests>=2.28.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    keywords='telegram bot api wrapper easy simplified synchronous'
)