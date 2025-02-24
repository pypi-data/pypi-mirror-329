from setuptools import setup, find_packages

setup(
    name="chATLAS_Benchmark",
    version="0.0.4",
    description="A Python package for LLM and RAG testing in high-energy physics applications (Originally for ATLAS in the chATLAS project).",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Ben Elliot",
    author_email="Ben.Elliot27@outlook.com",
    url="https://gitlab.cern.ch/belliot/chatlas-packages/",
    project_urls={
        "Documentation": "https://chatlas-packages.docs.cern.ch/chATLAS_Benchmark/"
    },
    packages=find_packages(include=["chATLAS_Benchmark", "chATLAS_Benchmark.*"]),
    install_requires=[
        "numpy~=1.26.4",
        "pandas~=2.2.3",
        "SQLAlchemy~=2.0.35",
        "nltk~=3.9.1",
        "torch~=2.4.1",
        "sentence_transformers~=3.2.0",
        "pathlib",  # Standard library, but sometimes included for compatibility
        "dataclasses; python_version<'3.7'",  # Needed for Python < 3.7
        "openai",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
