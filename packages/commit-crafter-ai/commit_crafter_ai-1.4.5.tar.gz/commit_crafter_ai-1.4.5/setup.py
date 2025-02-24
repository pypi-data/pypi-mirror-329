from setuptools import setup, find_packages

setup(
    name="commit-crafter-ai",
    version="1.4.5",
    author="Serhat Uzbas",
    author_email="serhatuzbas@gmail.com",
    description="AI-powered commit message generator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SerhatUzbas/commit-crafter-ai/",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    install_requires=[
        "typer[all]",
        "openai==1.57.4",
        "pyperclip",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "commit-crafter-ai=commit_crafter.commit_crafter:app",
        ],
    },
    python_requires=">=3.7",
)
