from setuptools import setup, find_packages

setup(
    name="BwETA",
    version="V0.13",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "transformers",
        "huggingface_hub",
        "numpy"
    ],
    description="A custom model testing module",
    author="Boring._.wicked",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)