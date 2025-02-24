from setuptools import setup, find_packages

setup(
    name="quickstart_cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "quickstart-cli=quickstart_cli.main:main",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool to generate project boilerplates.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/quickstart_cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
