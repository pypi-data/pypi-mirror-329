from setuptools import setup, find_packages

setup(
    name="BenchNLP",
    version="0.1.0",
    description="NLP Explainability Benchmarking Framework",
    author="Your Name",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "captum",
        "scikit-learn",
        "matplotlib",
        "datasets",
        "typing",
        "copy",
        "typing",
        "numpy",
        "pandas",
        "seaborn"
    ],
    entry_points={
        "console_scripts": ["explainer-benchmark=BenchNLP.cli:main"],
    },
)
