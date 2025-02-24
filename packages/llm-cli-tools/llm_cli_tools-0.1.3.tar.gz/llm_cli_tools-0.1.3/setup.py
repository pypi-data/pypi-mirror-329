from setuptools import setup, find_packages

setup(
    name="llm-cli-tools",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "click",
        "python-dotenv",
        "fastapi",
        "uvicorn",
        "pydantic",
        "requests",
        "beautifulsoup4",
        "openai",
        "anthropic",
        "mistralai",
        "ollama",
        "google-genai"
    ],
    entry_points={
        'console_scripts': [
            'llx=llx.cli:main',
        ],
    },
    author="Marco Campana",
    author_email="marco@xterm.it",
    description="A CLI tool to interact with various LLM APIs",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/marcocampana/llx",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)