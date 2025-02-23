from setuptools import setup, find_packages

CURRENT_VERSION = "0.1.0"
AUTHOR = "Kuqilin"
AUTHOR_EMAIL = "kuqilin_1@163.com"

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wcnm",
    version=CURRENT_VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description="A command line tool to get a random quote when you input \"cnm\".",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "requests",
        "subprocess"
    ],
    entry_points={
        "console_scripts": [
            "cnm = wcnm.main:main"
        ],
    },
)