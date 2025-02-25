from setuptools import setup, find_packages

setup(
    name="asyncconfigreader",
    version="0.6",
    install_requires=[
        "pynput==1.7.7"
    ],
    packages=find_packages(),
)

