## **📦 Packaging a Python CLI Tool for Distribution**

This guide explains **how to package and distribute a Python CLI tool** so others can install and use it like a native command (e.g., `mycli`).  
We’ll walk through:  
✅ Structuring the project  
✅ Writing `setup.py`  
✅ Adding a CLI entry point  
✅ Building and testing the package  
✅ Publishing it on **PyPI**  

---

### 🔹 **1. Project Structure for Packaging**

Organize your project with the following structure:

```
my_cli_tool/
│
├── mycli/                  # Python package
│   ├── __init__.py
│   └── cli.py              # CLI implementation
│
├── tests/                  # Unit tests
│   └── test_cli.py
│
├── setup.py                # Packaging configuration
├── pyproject.toml          # Optional modern build system file
├── README.md               # Project description for PyPI
├── requirements.txt        # Dependencies
├── LICENSE
└── .gitignore
```

---

### 🔹 **2. Writing `cli.py` – The CLI Entry Point**

In `mycli/cli.py`:

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Say hello from a CLI tool")
    parser.add_argument("name", help="Your name")
    args = parser.parse_args()
    print(f"Hello, {args.name}!")

if __name__ == "__main__":
    main()
```

---

### 🔹 **3. Creating `setup.py`**

In the project root:

```python
from setuptools import setup, find_packages

setup(
    name="my-cli-tool",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "mycli = mycli.cli:main"  # command = module:function
        ]
    },
    author="Name",
    author_email="name.surname@gmail.com",
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
```

✅ This tells `setuptools` how to build and install your CLI tool.  
✅ The `entry_points` block creates an executable command (`mycli`) that calls `cli.main()`.

---

### 🔹 **4. Creating `pyproject.toml` (Optional but Recommended)**

To comply with **PEP 517**, add this in the project root:

```toml
[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"
```

✅ This defines how to build the package (required by modern tools like `pip`, `twine`, and `build`).

---

### 🔹 **5. Installing and Testing Locally**

Install your tool in **editable mode**:

```bash
pip install -e .
```

✅ Now you can run:

```bash
mycli Alice
```

✅ Output:

```
Hello, Alice!
```

---

### 🔹 **6. Building the Package**

Install build tools:

```bash
pip install setuptools wheel
```

Then build the package:

```bash
python setup.py sdist bdist_wheel
```

✅ This generates files in the `dist/` folder:

```
dist/
├── my-cli-tool-0.1.0.tar.gz
└── my_cli_tool-0.1.0-py3-none-any.whl
```

---

### 🔹 **7. Publishing to PyPI**

#### ✅ Step 1: Create an account on [https://pypi.org](https://pypi.org)

#### ✅ Step 2: Install Twine

```bash
pip install twine
```

#### ✅ Step 3: Upload to Test PyPI (Optional)

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

✅ Use this for testing without publishing live.

#### ✅ Step 4: Upload to PyPI

```bash
twine upload dist/*
```

You will be prompted for your **PyPI username and password**.

---

### 🔹 **8. Installing the CLI Tool via pip**

Once published, anyone can install your tool like this:

```bash
pip install my-cli-tool
```

Then run it:

```bash
mycli Alice
```

✅ Your CLI tool is now globally available!

---

## 🔹 **Best Practices**

| Tip | Description |
|-----|-------------|
| ✅ Use `find_packages()` | Automatically includes all submodules |
| ✅ Include `README.md` | Shows up on PyPI page |
| ✅ Use semantic versioning | e.g., `0.1.0`, `1.0.0` |
| ✅ Test before uploading | Use `twine check dist/*` and `test.pypi.org` |
| ✅ Add `MANIFEST.in` if you want to include non-code files |

---

## 🔹 Example `requirements.txt`

```txt
argparse
```

---

## 📦 Summary

| Step | Action |
|------|--------|
| 1 | Organize your project structure |
| 2 | Write `cli.py` with a `main()` function |
| 3 | Create `setup.py` with `entry_points` |
| 4 | (Optional) Add `pyproject.toml` |
| 5 | Build the package using `setuptools` |
| 6 | Publish to PyPI using `twine` |
| 7 | Install with `pip` and run using your CLI command |

