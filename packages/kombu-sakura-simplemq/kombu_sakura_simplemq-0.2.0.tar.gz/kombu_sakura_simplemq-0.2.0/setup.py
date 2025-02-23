from setuptools import setup, find_packages

setup(
    name="kombu-sakura-simplemq",
    version="0.2.0",
    packages=find_packages(),
    install_requires=["kombu", "requests"],
)
