from setuptools import setup, find_packages

setup(
    name="text_classifier_sdk",
    version="0.1.4",
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "pandas",
        "scikit-learn",
        "requests"
    ],
    author="Ikenna Anikwe",
    author_email="ikennaedmundanikwe@gmail.com",
    description="A simple text classification SDK.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iyke0z/text-classifier-sdk",
    python_requires=">=3.11",
    license = "MIT",
)