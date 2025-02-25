from setuptools import setup, find_packages

setup(
    name="EvalXAI",
    version="0.1.0",
    description="NLP Explainability Benchmarking Framework",
    author="Kafaite Zahra Hussain",
    author_email="kafait.e.zahra@gmail.com",
    url="https://github.com/kafaite24/EvalXAI",
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
    ]
)
