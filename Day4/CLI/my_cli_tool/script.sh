#!/bin/bash

# Set project name
PROJECT_NAME="my_cli_tool"

# Create project structure
mkdir -p $PROJECT_NAME/{mycli,tests,logs}
cd $PROJECT_NAME

# Create __init__.py
touch mycli/__init__.py

# Create cli.py
cat <<EOF > mycli/cli.py
import argparse

def main():
    parser = argparse.ArgumentParser(description="Say hello from a CLI tool")
    parser.add_argument("name", help="Your name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
EOF

# Create setup.py
cat <<EOF > setup.py
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
EOF

# Create pyproject.toml
cat <<EOF > pyproject.toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"
EOF

# Create README.md
cat <<EOF > README.md
# My CLI Tool

A simple command-line interface tool written in Python using \`argparse\`.

## Usage

\`\`\`bash
mycli Alice
\`\`\`
EOF

# Create .gitignore
cat <<EOF > .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
*.egg-info/
dist/
build/
venv/
EOF

# Create requirements.txt
echo "argparse" > requirements.txt

# Create a sample test file
cat <<EOF > tests/test_cli.py
import unittest

def test_placeholder():
    assert True
EOF

# Optional: Create LICENSE file
cat <<EOF > LICENSE
MIT License
EOF

echo "✅ CLI tool project '$PROJECT_NAME' has been created!"
echo "👉 Next steps:"
echo "1. cd $PROJECT_NAME"
echo "2. pip install -e ."
echo "3. Run using: mycli YourName"
echo "4. Build with: python setup.py sdist bdist_wheel"
echo "5. Publish with: twine upload dist/*"