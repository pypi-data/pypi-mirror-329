from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Topic :: Games/Entertainment",
    "Topic :: Multimedia :: Graphics",
    "Topic :: Software Development"
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cliengine",
    version="0.0.7",
    description="A simple and limited game engine for the command-line interface.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    author="MinaRoblox",
    author_email="emanuelgardunomondragon@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=["pyperclip"]
)