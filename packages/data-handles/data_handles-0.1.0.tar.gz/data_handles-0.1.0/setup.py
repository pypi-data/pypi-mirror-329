from setuptools import setup, find_packages

setup(
    name="data_handles",
    version="0.1.0",
    author="Janish Pancholi",
    author_email="janish.pancholi11@gmail.com",
    description="A simple data handling and encryption package.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourgithub/crypto_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
