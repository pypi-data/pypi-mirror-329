from setuptools import setup, find_packages

setup(
    name="deploy-llm",
    version="0.0.2",
    packages=find_packages(),
    install_requires=[
        "click"
    ],
    entry_points={
        "console_scripts": [
            "llmdeploy=llmdeploy.cli:cli"
        ]
    },
    author="Ankit Gupta",
    author_email="devankitgupta01@gmail.com",
    description="A CLI tool to deploy and manage LLMs using Ollama.",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)