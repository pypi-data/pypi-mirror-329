from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="ml_gcam",
    version="0.2.2",
    description="gcam emulator",
    packages=find_packages(),
    url="https://github.com/hutchresearch/ml_climate_gcam22/tree/documentation",
    author="HutchResearch",
    author_email="brian.hutchinson@wwu.edu",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[
	"torch",
	"pytorch-cuda==1.12.1",
	"einops",
	"accelerate",
	"torchtyping",
	"scikit-learn",
	"seaborn",
	"tensorboard",
	"wandb",
	"polars>=0.20.19",
	"pandas",
	"pyarrow",
	"marimo",
	"gcamreader>=1.4.0",
	"pytest",
	"pytest-cov",
	"click",
	"rich",
	"tqdm",
	"python-dotenv",
	"python-configuration[toml]",
	"lxml",
	"geopandas>=0.9.0",
    ],
    python_requires=">=3.10",
    entry_points={
	'console_scripts': [
		'egcam = ml_gcam:__main__.py',
	]
    }

)
