# setup.py

from setuptools import setup, find_packages

setup(
    name="rag_pipeline",
    version="0.1.2",
    packages=find_packages(),
    install_requires=["openai", "faiss-cpu", "numpy", "pdfplumber"],
    author="Salim Khazem",
    author_email="salim.khazem@talan.com",
    description="A library for Retrieval-Augmented Generation with Azure OpenAI",
    url="https://github.com/salimkhazem/rag-pipeline",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
