from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="leanquant",
    version="0.1.1",
    author="Tianyi Zhang",
    author_email="tonyzhang617@gmail.com",
    description="The inference kernels for LeanQuant models.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "transformers>=4.38",
        "accelerate",
        "safetensors",
        "torch",
    ],
    extras_require={
        "cuda11": [
            "cupy-cuda11x",
        ],
        "cuda12": [
            "cupy-cuda12x",
        ],
    },
)
