from setuptools import setup, find_packages

setup(
    name="customGPTBW",
    version="0.1.50",
    packages=find_packages(),
    install_requires=[
        "tensorflow",
        "transformers",
        "tqdm",
        "psutil",
        "huggingface_hub",
        "datasets",
        "numpy"
    ],
    description="A private module for dataset loading and GPT training.",
    author="Boring._.wicked",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
    ],
)