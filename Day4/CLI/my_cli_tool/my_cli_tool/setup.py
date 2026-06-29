from setuptools import setup, find_packages

setup(
    name="my-cli-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mycli = mycli.cli:main"
        ]
    },
    author="Ali Mokh",
    author_email="ali.mokh.101@gmail.com",
    description="A simple example CLI tool",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my-cli-tool",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
)
