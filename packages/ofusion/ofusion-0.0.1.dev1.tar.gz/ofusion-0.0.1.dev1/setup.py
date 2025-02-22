import re
from setuptools import setup, find_packages

with open("ofusion/__init__.py", encoding="utf8") as f:
    version = re.search(r'__version__ = "(.*?)"', f.read()).group(1)

setup(
    name="ofusion",
    version=version,
    description="A Domain-Specific Language for High-Performance Creative Coding with openFrameworks",
    author="Bairui Su",
    author_email="subairui@icloud.com",
    url="https://github.com/yourusername/ofusion",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)