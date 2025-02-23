from setuptools import setup, find_packages

setup(
    name="cross_nli",
    version="0.1.0",
    author="Dimitris Gkoumas",
    author_email="gkoumasjim@gmail.com",
    description="A package for evaluating hallucination and coverage in generated outputs deploying NLI and LLM models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gkoumasd/cross_nli",
    packages=find_packages(),
    install_requires=[
        "torch",
        "numpy",
        "transformers",
        "tqdm",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)