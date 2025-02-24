from setuptools import setup, find_packages

VERSION = "0.2.25"
DESCRIPTION = "Common utils package. With some basic classes."
LONG_DESCRIPTION = "Package with common utils for new projects."

setup(
    name="common_utils_pkg",
    version=VERSION,
    author="John Johny",
    author_email="love.dev.2020@email.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=["apprise", "schedule", "boto3", "loguru", "pydantic", "pyjwt", "bcrypt"],
    keywords=["python"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
    ],
)
