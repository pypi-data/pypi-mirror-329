from setuptools import setup, find_packages

classifiers = [
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python"
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cliengine",
    version="0.0.4",
    description="A simple and limited game engine for the command-line interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Add this line!
    url="",
    author="MinaRoblox",
    author_email="emanuelgardunomondragon@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="",
    packages=find_packages(),
    install_requires=["pyperclip"]
)