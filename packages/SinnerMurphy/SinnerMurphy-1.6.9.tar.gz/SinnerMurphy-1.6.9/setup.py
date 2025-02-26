from setuptools import setup, find_packages
from datetime import datetime

setup(
    name="SinnerMurphy",
    version="1.6.9",  # Keep this in sync with __init__.py
    author="Sinner Murphy",
    author_email="sinnermurphy@hi2.in",
    description="A Powerful And Advance Telegram Bot By Sinner Murphy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourgithub/SinnerMurphy",
    packages=find_packages(),
    install_requires=[
        "telethon",
        "pymongo",
        "googletrans==4.0.0-rc1",
        "requests",
        "emoji",
        "gtts",
        "pytz",
    ],
    license="MIT",  # License type
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)

