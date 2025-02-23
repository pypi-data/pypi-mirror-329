from setuptools import setup, find_packages

setup(
    name="deploy-llm",
    version="0.1.5",
    packages=find_packages(),
    install_requires=[
        "click",
        "torch",
        "transformers"
    ],
    entry_points={
        "console_scripts": [
            "llmdeploy=cli:cli",
        ],
    },
    author="Ankit Gupta",
    description="CLI tool for deploying and running models from Ollama and Hugging Face",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
