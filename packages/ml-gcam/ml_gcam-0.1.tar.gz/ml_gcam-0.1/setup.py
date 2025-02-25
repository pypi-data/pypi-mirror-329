from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ml_gcam",
    version="0.0.10",
    description="gcam emulator",
    packages=find_packages(),
    url="https://github.com/hutchresearch/ml_climate_gcam22/tree/pnnl_published",
    author="HutchResearch",
    author_email="brian.hutchinson@wwu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.10",
)
