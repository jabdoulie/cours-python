


### **Course**: **Mastering Python for DevOps**

**Author**: Ali Mokh, PhD  
**Contact**: [Ali.mokh.101@gmail.com](mailto:Ali.mokh.101@gmail.com)

#### **Introduction**

Welcome to the **Mastering Python for DevOps** course! Over the next three days, we will take a deep dive into Python programming and its applications in DevOps workflows. This course is structured to equip you with both foundational programming skills and advanced techniques for developing and deploying Python-based applications.

This document is designed to provide a detailed understanding of Python programming and its application in DevOps workflows. It covers foundational Python concepts, advanced programming techniques, and practical tools used for building, testing, and deploying Python-based applications. By the end of this guide, you will have the skills and knowledge required to automate workflows, develop REST APIs, and implement CI/CD pipelines.

---

#### **Course Objectives**

By the end of this course, you will be able to:
1. Understand and apply Python programming fundamentals to solve real-world problems.
2. Set up and manage Python projects using virtual environments and dependency management.
3. Develop modular, testable Python applications using best practices.
4. Build RESTful APIs using Flask for scalable and robust applications.
5. Leverage containerization tools like Docker to package and deploy your Python applications.
6. Automate workflows using Makefiles for streamlined development.
7. Design and implement CI/CD pipelines with GitHub Actions.
8. Deploy Python-based microservices to cloud platforms such as Azure.

---

#### **Day-Wise Breakdown**

1. **Day 1**: Python Basics, Environment Setup, and Dependency Management.
   - Introduction to Python programming.
   - Setting up Python virtual environments.
   - Writing modular and reusable Python code.

2. **Day 2**: Modular Programming, Testing, and Containerization.
   - Writing testable code.
   - Introduction to Docker and containerization.
   - Building and running containerized applications.

3. **Day 3**: CI/CD Pipelines and Deployment.
   - Automating workflows using GitHub Actions.
   - Deploying Python applications to cloud platforms.
   - Final project implementation.

---

#### **Assessment and Assignments**

- **Homework 1 (Day 1)**: Python Basics and Project Setup.
- **Homework 2 (Day 2)**: Build and Containerize a Python Microservice.
- **Final Project (Day 3)**: Design, containerize, and deploy a Python-based microservice with CI/CD pipelines.

---

#### **Tools and Technologies**

- **Programming Language**: Python
- **Framework**: Flask
- **Containerization**: Docker
- **CI/CD**: GitHub Actions
- **Cloud Platforms**: Azure

---

#### **Learning Approach**

- **Interactive Lectures**: Each session will cover theoretical and practical aspects.
- **Hands-On Labs**: Apply what you learn with guided exercises.
- **Assignments**: Reinforce learning with real-world problems.

---
### **Table of Contents**

---

0. **Summary**  
   - Overview of the Guide  
   - Learning Outcomes  
   - Target Audience  
   - Prerequisites  

1. **Introduction to Python**  
   - Why Python for DevOps?  
   - Key Features of Python  
   - Setting Up Python  
   - Python in DevOps Workflows  

2. **Variables and Data Types**  
   - Defining Variables  
   - Python Data Types  
   - Type Conversion and Checking  
   - Collections: Lists, Tuples, Dictionaries, and Sets  

3. **Conditionals and Loops**  
   - Control Flow with `if`, `else`, and `elif`  
   - Loops: `for` and `while`  
   - Control Statements: `break`, `continue`, `else` in Loops  
   - Best Practices for Control Flow  

4. **Functions and Modules**  
   - Defining and Using Functions  
   - Parameters, Arguments, and Return Values  
   - Organizing Code with Modules  
   - Using Built-in and Custom Modules  

5. **File Handling**  
   - Reading and Writing Files  
   - Working with JSON Files  
   - Managing File Paths  
   - Best Practices for File Handling  

6. **Error Handling**  
   - Understanding Exceptions  
   - Using `try`, `except`, `else`, and `finally`  
   - Raising and Catching Custom Exceptions  
   - Logging Errors   

7. **Testing Basics**  
   - Importance of Testing  
   - Writing Unit Tests with `unittest`  
   - Testing Exceptions and Edge Cases  
   - Best Practices for Testing  

8. **REST API Development**  
    - Setting Up Flask  
    - Building RESTful Endpoints (`GET`, `POST`, `PUT`, `DELETE`)  
    - Validating Input and Error Handling  
    - Best Practices for API Development  

9. **Object-Oriented Programming (OOP)**  
   - Classes and Objects  
   - Attributes and Methods  
   - Inheritance and Encapsulation  
   - Polymorphism and Abstraction 
---

### **Content Overview**

1. **Introduction to Python**:
   - Learn why Python is a preferred language for DevOps.
   - Understand Python's features, installation, and setup.

2. **Variables and Data Types**:
   - Explore how to define variables and work with Python’s diverse data types.

3. **Conditionals and Loops**:
   - Master control flow using `if`, `else`, `for`, and `while`.

4. **Functions and Modules**:
   - Develop reusable, modular code by defining functions and creating modules.

5. **File Handling**:
   - Read from and write to text, JSON, and binary files effectively.

6. **Error Handling**:
   - Manage exceptions gracefully using `try`, `except`, `else`, and `finally`.

7. **Object-Oriented Programming (OOP)**:
   - Dive into classes, objects, inheritance, encapsulation, and polymorphism.

8. **Testing Basics**:
   - Ensure code reliability with Python’s `unittest` framework, including test case design and mocking.

9. **REST API Development**:
   - Build RESTful APIs using Flask, including routing, input validation, and best practices.

---

### **Learning Outcomes**

After completing this guide, you will be able to:
- Develop Python scripts and applications with modular and testable code.
- Handle files and errors efficiently in Python.
- Build RESTful APIs for robust and scalable applications.
- Apply OOP principles to design reusable and maintainable code.
- Write and execute unit tests to ensure code quality.
- Automate workflows and deploy applications using CI/CD pipelines.

---

### **Target Audience**

This guide is designed for:
- Beginners looking to build a strong foundation in Python.
- Developers transitioning into DevOps roles.
- Professionals aiming to automate workflows and streamline deployments.

---

### **Prerequisites**

Before diving into this guide, ensure you have:
- Basic knowledge of programming concepts.
- Python installed on your system.
- A code editor (e.g., VS Code, PyCharm).

---



## **1. Introduction to Python**

---

#### **Introduction**

Python is a versatile, high-level programming language that emphasizes readability and simplicity. Its ease of use and extensive ecosystem make it a popular choice for various fields, including web development, data science, artificial intelligence, and DevOps.

In this section, we will introduce Python, its key features, and why it is particularly valuable in DevOps workflows.

---

#### **Why Python?**

Python stands out because of its:
1. **Ease of Learning**: Python's syntax is clean and intuitive, making it ideal for beginners.
2. **Extensive Libraries**: Python offers libraries for virtually every task, from web development (`Flask`, `Django`) to system automation (`os`, `shutil`).
3. **Cross-Platform Compatibility**: Python works seamlessly on Windows, macOS, and Linux.
4. **Large Community**: Python has a vast and active community that contributes to its development and offers support.

---

#### **Key Features of Python**

1. **Simple and Readable Syntax**:
   - Python code is designed to be readable, making it accessible even for beginners.
   - Example:
     ```python
     # This code prints "Hello, World!"
     print("Hello, World!")
     ```

2. **Interpreted Language**:
   - Python executes code line by line, allowing for quick debugging and testing.

3. **Dynamic Typing**:
   - No need to declare variable types explicitly. Python determines the type at runtime.
   - Example:
     ```python
     name = "Alice"  # String
     age = 30        # Integer
     height = 5.6    # Float
     ```

4. **Extensive Standard Library**:
   - Python includes modules for handling tasks like file I/O, math operations, and regular expressions.
   - Example:
     ```python
     import math
     print(math.sqrt(16))  # Outputs: 4.0
     ```

5. **Support for Multiple Paradigms**:
   - Python supports procedural, object-oriented, and functional programming styles.

6. **Large Ecosystem**:
   - Thousands of third-party libraries are available via **PyPI** (Python Package Index).

---

#### **Python in DevOps**

Python is widely used in DevOps for tasks like:
- **Automation**:
  - Writing scripts to automate repetitive tasks like backups or deployments.
  - Example:
    ```python
    import os
    os.system("echo 'Hello, DevOps!'")
    ```
- **Configuration Management**:
  - Tools like **Ansible** use Python for managing infrastructure.
- **Monitoring and Logging**:
  - Python's libraries like `psutil` and `logging` make it easy to monitor system performance and log events.
- **Building CI/CD Pipelines**:
  - Python integrates well with tools like Jenkins, GitHub Actions, and CircleCI.
- **Testing**:
  - Frameworks like `unittest` and `pytest` are used to automate testing.

---

#### **Setting Up Python**

To start coding in Python, follow these steps:

1. **Install Python**:
   - Download the latest version of Python from [python.org](https://www.python.org/).
   - Verify the installation:
     ```bash
     python3 --version
     ```

2. **Set Up a Code Editor**:
   - Recommended editors:
     - **VS Code**: Lightweight and feature-rich.
     - **PyCharm**: Python-specific IDE.

3. **Install Packages**:
   - Use `pip`, Python's package manager, to install libraries:
     ```bash
     pip install flask
     ```

4. **Write Your First Python Script**:
   - Save the following code in a file named `hello.py`:
     ```python
     print("Hello, World!")
     ```
   - Run the script:
     ```bash
     python3 hello.py
     ```

---

#### **Advantages of Python Over Other Languages**

| Feature            | Python                          | Other Languages                 |
|--------------------|---------------------------------|---------------------------------|
| **Ease of Use**    | Simple and beginner-friendly    | Often complex for beginners     |
| **Versatility**    | Supports multiple paradigms     | Limited to one paradigm (e.g., Java) |
| **Library Support**| Extensive libraries and frameworks | Limited or language-specific    |
| **Community**      | Large and active               | Smaller or niche communities    |

---

#### **Best Practices for Learning Python**

1. **Start Small**:
   - Focus on writing small scripts to automate tasks.
2. **Practice Regularly**:
   - Solve coding challenges on platforms like **HackerRank** or **LeetCode**.
3. **Use Virtual Environments**:
   - Isolate dependencies for each project using `venv`.
   - Example:
     ```bash
     python3 -m venv myenv
     source myenv/bin/activate
     ```
4. **Read Python Documentation**:
   - Familiarize yourself with [Python's official documentation](https://docs.python.org/3/).

---

## **2. Variables and Data Types**



#### **2.1. Introduction to Variables**

A variable in Python is a name assigned to a value. It acts as a container to store data that can be manipulated or retrieved later.

Key Features:
1. Python is dynamically typed: You don’t need to specify the data type.
2. Variables can store different types of data, such as numbers, text, or objects.

**Example**:
```python
name = "Alice"  # String
age = 25        # Integer
height = 5.7    # Float

print(f"{name} is {age} years old and {height} feet tall.")
```

**Output**:
```plaintext
Alice is 25 years old and 5.7 feet tall.
```

---

#### **2.2. Rules for Naming Variables**
1. Variable names must start with a letter or an underscore (_).
2. They can only contain alphanumeric characters and underscores (e.g., `name_1`).
3. Variable names are case-sensitive (`name` and `Name` are different).
4. Reserved keywords (e.g., `if`, `while`) cannot be used as variable names.

**Valid Examples**:
```python
_name = "DevOps"
user123 = 42
```

**Invalid Examples**:
```python
1name = "Error"  # Starts with a number
if = "Error"     # Uses a reserved keyword
```

---

#### **2.3. Data Types in Python**

Python supports the following data types:

| **Data Type** | **Description**                            | **Example**           |
|---------------|--------------------------------------------|-----------------------|
| `int`         | Integer numbers                           | `10`, `-5`            |
| `float`       | Decimal numbers                           | `3.14`, `-0.01`       |
| `str`         | Strings of text                           | `"hello"`, `"123"`    |
| `bool`        | Boolean values                            | `True`, `False`       |
| `list`        | Ordered, mutable collection               | `[1, 2, 3]`           |
| `tuple`       | Ordered, immutable collection             | `(1, 2, 3)`           |
| `dict`        | Key-value pairs                           | `{"key": "value"}`    |
| `set`         | Unordered collection of unique elements   | `{1, 2, 3}`           |

---

#### **Examples of Data Types**

**Integer and Float**:
```python
x = 42        # Integer
pi = 3.14159  # Float
print(x, pi)
```

**Output**:
```plaintext
42 3.14159
```

**String**:
```python
greeting = "Hello, DevOps!"
print(greeting.upper())
```

**Output**:
```plaintext
HELLO, DEVOPS!
```

**Boolean**:
```python
is_active = True
is_admin = False
print(is_active and is_admin)
```

**Output**:
```plaintext
False
```

---

#### **Type Conversion**

Convert data types using built-in functions like `int()`, `float()`, or `str()`.

**Example**:
```python
x = "123"
y = int(x)  # Convert string to integer
z = float(x)  # Convert string to float

print(y + 1)  # Output: 124
print(z + 1)  # Output: 124.0
```

---

#### **Type Checking**

Use `type()` to check the type of a variable.

**Example**:
```python
x = 42
print(type(x))  # Output: <class 'int'>
```

---

#### **2.4. Collections: Lists, Tuples, Dictionaries, and Sets**

**Lists**:
- Ordered and mutable.
- Example:
  ```python
  fruits = ["apple", "banana", "cherry"]
  fruits.append("orange")
  print(fruits)
  ```
  **Output**:
  ```plaintext
  ['apple', 'banana', 'cherry', 'orange']
  ```

**Tuples**:
- Ordered and immutable.
- Example:
  ```python
  coordinates = (10, 20)
  print(coordinates[0])
  ```
  **Output**:
  ```plaintext
  10
  ```

**Dictionaries**:
- Key-value pairs for fast lookups.
- Example:
  ```python
  user = {"name": "Alice", "age": 25}
  print(user["name"])
  ```
  **Output**:
  ```plaintext
  Alice
  ```

**Sets**:
- Unordered collection of unique elements.
- Example:
  ```python
  unique_numbers = {1, 2, 2, 3}
  print(unique_numbers)
  ```
  **Output**:
  ```plaintext
  {1, 2, 3}
  ```

---

#### **Best Practices for Variables**
1. Use meaningful names:
   ```python
   salary = 50000  # Clear and descriptive
   ```
2. Avoid using single-letter names, except in loops.
3. Follow naming conventions (`snake_case` for variables):
   ```python
   total_sales = 1000
   ```

---

## **3. Conditionals and Loops**

---

#### **Introduction**

Conditionals and loops are fundamental programming constructs that allow you to control the flow of your program. They enable you to execute specific blocks of code based on conditions or to repeat actions multiple times.

---

### **3.1. Conditionals**

Conditionals allow you to make decisions in your code based on logical expressions.

#### **`if` Statements**

The `if` statement executes a block of code if the condition is `True`.

**Syntax**:
```python
if condition:
    # Code block to execute
```

**Example**:
```python
x = 10
if x > 5:
    print("x is greater than 5")
```

**Output**:
```plaintext
x is greater than 5
```

---

#### **`if-else` Statements**

The `else` block executes when the condition is `False`.

**Syntax**:
```python
if condition:
    # Code block if condition is True
else:
    # Code block if condition is False
```

**Example**:
```python
x = 3
if x > 5:
    print("x is greater than 5")
else:
    print("x is not greater than 5")
```

**Output**:
```plaintext
x is not greater than 5
```

---

#### **`if-elif-else` Statements**

The `elif` (else if) block checks multiple conditions.

**Syntax**:
```python
if condition1:
    # Code block if condition1 is True
elif condition2:
    # Code block if condition2 is True
else:
    # Code block if no conditions are True
```

**Example**:
```python
x = 5
if x > 5:
    print("x is greater than 5")
elif x == 5:
    print("x is equal to 5")
else:
    print("x is less than 5")
```

**Output**:
```plaintext
x is equal to 5
```

---

#### **Logical Operators**

Logical operators are used to combine multiple conditions:
- **`and`**: All conditions must be `True`.
- **`or`**: At least one condition must be `True`.
- **`not`**: Negates the condition.

**Example**:
```python
x = 10
y = 20

if x > 5 and y > 15:
    print("Both conditions are True")
```

**Output**:
```plaintext
Both conditions are True
```

---

### **3.2. Loops**

Loops allow you to repeat a block of code multiple times.

---

#### **`for` Loops**

A `for` loop iterates over a sequence (e.g., list, range, string).

**Syntax**:
```python
for variable in sequence:
    # Code block to execute
```

**Example**:
```python
for i in range(5):
    print(i)
```

**Output**:
```plaintext
0
1
2
3
4
```

---

#### **Iterating Over a List**

**Example**:
```python
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)
```

**Output**:
```plaintext
apple
banana
cherry
```

---

#### **`while` Loops**

A `while` loop continues executing as long as its condition is `True`.

**Syntax**:
```python
while condition:
    # Code block to execute
```

**Example**:
```python
x = 0
while x < 5:
    print(x)
    x += 1
```

**Output**:
```plaintext
0
1
2
3
4
```

---

### **3.3. Control Statements**

Control statements modify the execution flow inside loops.

---

#### **`break`**

The `break` statement exits a loop immediately.

**Example**:
```python
for i in range(10):
    if i == 5:
        break
    print(i)
```

**Output**:
```plaintext
0
1
2
3
4
```

---

#### **`continue`**

The `continue` statement skips the current iteration and proceeds to the next.

**Example**:
```python
for i in range(5):
    if i == 2:
        continue
    print(i)
```

**Output**:
```plaintext
0
1
3
4
```

---

#### **`else` with Loops**

You can use `else` with loops to execute code after the loop finishes, unless a `break` is encountered.

**Example**:
```python
for i in range(5):
    print(i)
else:
    print("Loop completed without interruption")
```

**Output**:
```plaintext
0
1
2
3
4
Loop completed without interruption
```

---

### **3.4. Nested Loops**

You can nest loops to iterate over multiple sequences.

**Example**:
```python
for i in range(2):
    for j in range(3):
        print(f"i={i}, j={j}")
```

**Output**:
```plaintext
i=0, j=0
i=0, j=1
i=0, j=2
i=1, j=0
i=1, j=1
i=1, j=2
```

---

### **3.5. Best Practices for Conditionals and Loops**

1. **Avoid Infinite Loops**:
   - Ensure `while` loops have a condition that eventually becomes `False`.

2. **Use Meaningful Loop Variables**:
   - Instead of generic names like `i`, use descriptive names when iterating over collections.

3. **Minimize Nesting**:
   - Deeply nested loops and conditionals can make code harder to read and maintain.

4. **Use List Comprehensions (Where Possible)**:
   - Simplify loops using list comprehensions for concise, readable code.
   - Example:
     ```python
     squares = [x**2 for x in range(5)]
     print(squares)
     ```
     **Output**:
     ```plaintext
     [0, 1, 4, 9, 16]
     ```

---

## **4. Functions and Modules**

---

#### **1. Functions**

Functions are reusable blocks of code that perform a specific task. They help to organize code into modular, manageable parts.

---

#### **Defining a Function**

A function is defined using the `def` keyword, followed by the function name and parentheses containing optional parameters.

**Syntax**:
```python
def function_name(parameters):
    # Code block
    return value
```

**Example**:
```python
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
```

**Output**:
```plaintext
Hello, Alice!
```

---

#### **Parameters and Arguments**

1. **Positional Parameters**:
   - Arguments are matched by their position in the function call.
   **Example**:
   ```python
   def add(a, b):
       return a + b

   print(add(5, 3))  # Output: 8
   ```

2. **Default Parameters**:
   - Assign default values to parameters.
   **Example**:
   ```python
   def greet(name="Guest"):
       return f"Hello, {name}!"

   print(greet())          # Output: Hello, Guest!
   print(greet("Alice"))   # Output: Hello, Alice!
   ```

3. **Keyword Arguments**:
   - Pass arguments using their names.
   **Example**:
   ```python
   def divide(a, b):
       return a / b

   print(divide(b=10, a=2))  # Output: 0.2
   ```

4. **Variable-Length Arguments**:
   - Use `*args` for a tuple of positional arguments.
   - Use `**kwargs` for a dictionary of keyword arguments.
   **Example**:
   ```python
   def summarize(*args, **kwargs):
       print("Args:", args)
       print("Kwargs:", kwargs)

   summarize(1, 2, 3, name="Alice", age=25)
   ```

   **Output**:
   ```plaintext
   Args: (1, 2, 3)
   Kwargs: {'name': 'Alice', 'age': 25}
   ```

---

#### **Return Values**

A function can return a value using the `return` statement.

**Example**:
```python
def square(x):
    return x * x

result = square(4)
print(result)  # Output: 16
```

---

#### **Lambda Functions**

A lambda function is a short, anonymous function defined using the `lambda` keyword.

**Example**:
```python
square = lambda x: x * x
print(square(5))  # Output: 25
```

---

#### **Scope and Lifetime of Variables**

1. **Local Variables**:
   - Defined within a function and accessible only there.
2. **Global Variables**:
   - Defined outside a function and accessible throughout the program.
   **Example**:
   ```python
   x = 10  # Global variable

   def modify():
       global x
       x = 20  # Modify global variable

   modify()
   print(x)  # Output: 20
   ```

---

### **2. Modules**

Modules are Python files containing reusable functions, classes, or variables. They help organize code into separate files.

---

#### **Importing a Module**

Use the `import` keyword to include a module.

**Example**:
```python
import math

print(math.sqrt(16))  # Output: 4.0
```

---

#### **Creating a Custom Module**

1. Create a file named `utils.py`:
   ```python
   def add(a, b):
       return a + b
   ```

2. Import and use the module:
   ```python
   from utils import add

   print(add(5, 3))  # Output: 8
   ```

---

#### **Built-in Modules**

Python provides many built-in modules. Some commonly used ones are:
- **`os`**: Interacting with the operating system.
  ```python
  import os
  print(os.getcwd())  # Prints current working directory
  ```
- **`sys`**: System-specific parameters and functions.
  ```python
  import sys
  print(sys.version)  # Prints Python version
  ```
- **`random`**: Generating random numbers.
  ```python
  import random
  print(random.randint(1, 10))  # Random number between 1 and 10
  ```
- **`datetime`**: Working with dates and times.
  ```python
  from datetime import datetime
  print(datetime.now())  # Prints current date and time
  ```

---

#### **Best Practices for Functions and Modules**

1. Use meaningful names for functions and variables.
2. Keep functions small and focused on a single task.
3. Document functions with comments or docstrings.
   **Example**:
   ```python
   def add(a, b):
       """
       Adds two numbers and returns the result.
       """
       return a + b
   ```
4. Avoid excessive global variables; use parameters and return values instead.
5. Organize related functions into modules.

---

## **5. File Handling**

---

#### **Introduction**

File handling in Python allows you to read from and write to files, which is essential for storing and retrieving data. Python provides built-in methods for managing files, supporting various file formats like `.txt`, `.csv`, `.json`, and more.

---

### **1. Basics of File Handling**

Python uses the built-in `open()` function to handle files. Files can be opened in different modes:

| **Mode** | **Description**                 |
|----------|---------------------------------|
| `"r"`    | Read (default mode)            |
| `"w"`    | Write (overwrites existing content) |
| `"a"`    | Append (adds to existing content) |
| `"x"`    | Create (fails if the file exists) |
| `"rb"`   | Read in binary mode            |
| `"wb"`   | Write in binary mode           |

**Syntax**:
```python
file = open("filename.txt", mode)
# Perform file operations
file.close()
```

---

### **2. Writing to a File**

Use the `write()` method to add content to a file.

**Example**:
```python
with open("example.txt", "w") as file:
    file.write("Hello, World!")
```

- The `with` statement ensures the file is properly closed after writing.

---

### **3. Reading from a File**

Use the `read()` or `readlines()` methods to retrieve content.

**Example**:
```python
with open("example.txt", "r") as file:
    content = file.read()
    print(content)
```

**Output**:
```plaintext
Hello, World!
```

**Reading Line by Line**:
```python
with open("example.txt", "r") as file:
    for line in file:
        print(line.strip())  # Strip removes extra whitespace
```

---

### **4. Appending to a File**

Use the `"a"` mode to append data without overwriting existing content.

**Example**:
```python
with open("example.txt", "a") as file:
    file.write("\nThis is an additional line.")
```

---

### **5. Working with Binary Files**

Binary files handle data such as images, videos, or non-text content.

**Writing Binary Data**:
```python
with open("image.jpg", "rb") as file:
    content = file.read()

with open("copy.jpg", "wb") as new_file:
    new_file.write(content)
```

---

### **6. Managing File Paths**

Python’s `os` and `pathlib` modules help manage file paths.

**Example**:
```python
import os

# Check if a file exists
if os.path.exists("example.txt"):
    print("File exists")
else:
    print("File does not exist")

# Get the absolute path
print(os.path.abspath("example.txt"))
```

---

### **7. Working with JSON Files**

The `json` module is used to work with JSON (JavaScript Object Notation) files.

**Writing JSON**:
```python
import json

data = {"name": "Alice", "age": 30}
with open("data.json", "w") as file:
    json.dump(data, file)
```

**Reading JSON**:
```python
with open("data.json", "r") as file:
    data = json.load(file)
    print(data)
```

**Output**:
```plaintext
{'name': 'Alice', 'age': 30}
```

---

### **8. Handling Exceptions in File Operations**

Errors can occur if a file does not exist or if there are permission issues. Use `try-except` blocks to handle these gracefully.

**Example**:
```python
try:
    with open("nonexistent.txt", "r") as file:
        content = file.read()
except FileNotFoundError:
    print("The file does not exist.")
```

**Output**:
```plaintext
The file does not exist.
```

---

### **9. Cleaning Up Temporary Files**

For temporary files, use the `tempfile` module.

**Example**:
```python
import tempfile

with tempfile.NamedTemporaryFile(delete=True) as temp_file:
    temp_file.write(b"Temporary content")
    print(temp_file.name)  # Path to the temporary file
```

---

### **10. Best Practices for File Handling**

1. Always use the `with` statement for automatic file closure.
2. Use meaningful names for files and paths.
3. Validate file existence before reading or writing.
4. Handle exceptions to avoid program crashes.
5. Use relative paths for portability, or `os.path` for cross-platform compatibility.

---

### **Examples Summary**

1. **Write to a File**:
   ```python
   with open("example.txt", "w") as file:
       file.write("Hello, DevOps!")
   ```

2. **Read from a File**:
   ```python
   with open("example.txt", "r") as file:
       print(file.read())
   ```

3. **Append to a File**:
   ```python
   with open("example.txt", "a") as file:
       file.write("\nAppended content.")
   ```

4. **Handle JSON Data**:
   ```python
   import json
   data = {"task": "learn Python"}
   with open("tasks.json", "w") as file:
       json.dump(data, file)
   ```

---
## **6. Error Handling**

---

#### **Introduction**

Error handling in Python allows you to manage and respond to runtime errors gracefully, ensuring that your program can handle unexpected situations without crashing.

Python provides a structured way to handle exceptions using `try`, `except`, `else`, and `finally` blocks.

---

### **1. What Are Exceptions?**

An exception is an event that disrupts the normal flow of a program. Common exceptions include:
- **`ZeroDivisionError`**: Dividing by zero.
- **`FileNotFoundError`**: Attempting to access a file that doesn’t exist.
- **`KeyError`**: Accessing a non-existent dictionary key.
- **`ValueError`**: Passing the wrong type of value.

**Example of an Exception**:
```python
print(10 / 0)  # Raises ZeroDivisionError
```

**Output**:
```plaintext
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ZeroDivisionError: division by zero
```

---

### **2. Handling Exceptions**

#### **Basic Syntax**

The `try` block contains the code that may raise an exception. The `except` block defines how to handle the exception.

**Syntax**:
```python
try:
    # Code that may raise an exception
except ExceptionType:
    # Code to handle the exception
```

**Example**:
```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

**Output**:
```plaintext
Cannot divide by zero!
```

---

#### **Handling Multiple Exceptions**

You can handle multiple exceptions by specifying them in separate `except` blocks or using a tuple.

**Example**:
```python
try:
    value = int("abc")
except ValueError:
    print("Invalid input!")
except ZeroDivisionError:
    print("Cannot divide by zero!")
```

**Output**:
```plaintext
Invalid input!
```

---

#### **Using `else`**

The `else` block executes if no exception occurs.

**Example**:
```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Cannot divide by zero!")
else:
    print("The result is:", result)
```

**Output**:
```plaintext
The result is: 5.0
```

---

#### **Using `finally`**

The `finally` block executes regardless of whether an exception occurs, making it ideal for cleanup tasks.

**Example**:
```python
try:
    file = open("example.txt", "r")
    content = file.read()
except FileNotFoundError:
    print("File not found!")
finally:
    print("Execution finished.")
```

**Output**:
```plaintext
File not found!
Execution finished.
```

---

### **3. Raising Exceptions**

You can raise exceptions intentionally using the `raise` keyword.

**Example**:
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

try:
    print(divide(10, 0))
except ValueError as e:
    print(e)
```

**Output**:
```plaintext
Cannot divide by zero!
```

---

### **4. Custom Exceptions**

Define custom exceptions by creating a class that inherits from `Exception`.

**Example**:
```python
class NegativeNumberError(Exception):
    def __init__(self, message="Negative numbers are not allowed"):
        self.message = message
        super().__init__(self.message)

try:
    number = -10
    if number < 0:
        raise NegativeNumberError()
except NegativeNumberError as e:
    print(e)
```

**Output**:
```plaintext
Negative numbers are not allowed
```

---

### **5. Best Practices for Error Handling**

1. **Catch Specific Exceptions**:
   - Avoid using a generic `except` block unless necessary.
   - Example:
     ```python
     try:
         result = 10 / 0
     except ZeroDivisionError:
         print("Cannot divide by zero!")
     ```

2. **Provide Meaningful Error Messages**:
   - Inform users about the error and how to fix it.

3. **Avoid Silent Failures**:
   - Always log errors instead of ignoring them.

4. **Use `finally` for Cleanup**:
   - Release resources like files, sockets, or database connections.

5. **Raise Custom Exceptions for Business Logic**:
   - Example:
     ```python
     if salary < 0:
         raise ValueError("Salary cannot be negative.")
     ```

---

### **6. Logging Errors**

Use the `logging` module to capture errors instead of printing them.

**Example**:
```python
import logging

logging.basicConfig(filename="app.log", level=logging.ERROR)

try:
    result = 10 / 0
except ZeroDivisionError as e:
    logging.error(f"Error occurred: {e}")
```

**Output (in `app.log`)**:
```plaintext
ERROR:root:Error occurred: division by zero
```

---

### **Examples Summary**

1. **Basic Try-Except**:
   ```python
   try:
       print(10 / 0)
   except ZeroDivisionError:
       print("Cannot divide by zero!")
   ```

2. **Raising an Exception**:
   ```python
   if age < 0:
       raise ValueError("Age cannot be negative.")
   ```

3. **Logging Errors**:
   ```python
   import logging
   logging.error("An error occurred.")
   ```

---


## **7: Testing Basics**

---

#### **Introduction**

Testing ensures that your code works as expected and helps prevent bugs during development or after changes. Python provides built-in tools and frameworks like `unittest` for writing and running test cases.

---

### **1. Why Testing is Important**

1. **Improves Code Reliability**:
   - Detects bugs and prevents regressions.
2. **Simplifies Debugging**:
   - Pinpoints failing components.
3. **Ensures Maintainability**:
   - Confidence in making changes or adding features.
4. **Encourages Modularity**:
   - Writing testable code leads to better design.

---

### **2. Types of Tests**

1. **Unit Tests**:
   - Test individual units of code (e.g., functions, classes).
   - Focused on small, isolated components.

2. **Integration Tests**:
   - Test how different modules or components work together.

3. **End-to-End Tests**:
   - Test the entire application workflow from start to finish.

4. **Regression Tests**:
   - Ensure that new changes don’t break existing functionality.

---

### **3. The `unittest` Framework**

Python's `unittest` is a built-in framework for writing and running tests.

#### **Basic Structure of a Test Case**

1. Import `unittest`.
2. Create a test class inheriting from `unittest.TestCase`.
3. Define test methods starting with `test_`.

**Example**:
```python
import unittest

def add(a, b):
    return a + b

class TestMathFunctions(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)  # Test if 2 + 3 = 5

if __name__ == "__main__":
    unittest.main()
```

**Output**:
```plaintext
.
----------------------------------------------------------------------
Ran 1 test in 0.001s

OK
```

---

#### **Common Assertions**

| **Assertion Method**      | **Description**                                 |
|---------------------------|-----------------------------------------------|
| `assertEqual(a, b)`       | Asserts `a == b`.                             |
| `assertNotEqual(a, b)`    | Asserts `a != b`.                             |
| `assertTrue(x)`           | Asserts `x` is `True`.                        |
| `assertFalse(x)`          | Asserts `x` is `False`.                       |
| `assertIsNone(x)`         | Asserts `x` is `None`.                        |
| `assertRaises(Exception)` | Asserts an exception is raised in a block.    |

**Example**:
```python
class TestAssertions(unittest.TestCase):
    def test_assertions(self):
        self.assertTrue(10 > 5)
        self.assertEqual("Python".lower(), "python")
```

---

### **4. Testing a Function**

Let’s write tests for a basic function that multiplies two numbers.

**Function Code** (`utils.py`):
```python
def multiply(a, b):
    return a * b
```

**Test Code** (`test_utils.py`):
```python
import unittest
from utils import multiply

class TestUtils(unittest.TestCase):
    def test_multiply_positive(self):
        self.assertEqual(multiply(2, 3), 6)

    def test_multiply_negative(self):
        self.assertEqual(multiply(-2, 3), -6)

    def test_multiply_zero(self):
        self.assertEqual(multiply(0, 10), 0)

if __name__ == "__main__":
    unittest.main()
```

---

### **5. Testing Exceptions**

Use `assertRaises` to test if a function raises an expected exception.

**Example**:
```python
def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero!")
    return a / b

class TestDivision(unittest.TestCase):
    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(10, 0)
```

---

### **6. Running Tests**

Run all tests in a file:
```bash
python -m unittest test_utils.py
```

Discover and run all tests in the current directory:
```bash
python -m unittest discover
```

---

### **7. Mocking**

Mocking allows you to replace parts of your application during testing, such as simulating database queries or API calls.

**Example**:
```python
from unittest.mock import patch

def get_user_data(api_url):
    # Simulate an API call
    return {"name": "Alice"}

class TestAPI(unittest.TestCase):
    @patch("utils.get_user_data")
    def test_get_user_data(self, mock_get_user_data):
        mock_get_user_data.return_value = {"name": "Mocked Alice"}
        result = get_user_data("https://api.example.com/user")
        self.assertEqual(result["name"], "Mocked Alice")
```

---

### **8. Best Practices for Testing**

1. **Write Tests for Every Function**:
   - Ensure all critical functionality is covered.
2. **Keep Tests Independent**:
   - Avoid dependencies between tests.
3. **Use Meaningful Test Names**:
   - Clearly indicate the test's purpose.
4. **Run Tests Frequently**:
   - Detect bugs early by testing during development.
5. **Test Edge Cases**:
   - Include boundary conditions and invalid inputs.

---

### **9. Example Summary**

1. **Testing Addition**:
   ```python
   def add(a, b):
       return a + b

   class TestAdd(unittest.TestCase):
       def test_add(self):
           self.assertEqual(add(3, 4), 7)
   ```

2. **Testing Exceptions**:
   ```python
   def divide(a, b):
       if b == 0:
           raise ValueError("Division by zero!")
       return a / b

   class TestDivide(unittest.TestCase):
       def test_divide_by_zero(self):
           with self.assertRaises(ValueError):
               divide(10, 0)
   ```

3. **Running Tests**:
   ```bash
   python -m unittest test_utils.py
   ```

---

## **8. REST API Development**

---

#### **Introduction**

A REST API (Representational State Transfer Application Programming Interface) allows communication between systems using standard HTTP methods like `GET`, `POST`, `PUT`, and `DELETE`. Python provides lightweight frameworks like Flask for building REST APIs quickly and effectively.

This section covers the essentials of REST API development with Flask, including routing, handling requests, and sending responses.

---

### **1. Setting Up Flask**

1. **Install Flask**:
   ```bash
   pip install flask
   ```

2. **Create a Simple Flask App**:
   **`app.py`**:
   ```python
   from flask import Flask

   app = Flask(__name__)

   @app.route("/")
   def home():
       return "Welcome to the REST API!"

   if __name__ == "__main__":
       app.run(debug=True)
   ```

3. **Run the App**:
   ```bash
   python app.py
   ```
   Open a browser and go to `http://127.0.0.1:5000`.

---

### **2. Basic REST API Endpoints**

#### **Common HTTP Methods**

| **Method**  | **Purpose**                           |
|-------------|---------------------------------------|
| `GET`       | Retrieve data                         |
| `POST`      | Submit new data                       |
| `PUT`       | Update existing data                  |
| `DELETE`    | Remove data                           |

---

#### **GET Request**

Retrieve data from the server.

**Example**:
```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users", methods=["GET"])
def get_users():
    users = [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]
    return jsonify(users)

if __name__ == "__main__":
    app.run(debug=True)
```

- **URL**: `http://127.0.0.1:5000/users`
- **Response**:
  ```json
  [
      {"id": 1, "name": "Alice"},
      {"id": 2, "name": "Bob"}
  ]
  ```

---

#### **POST Request**

Submit new data to the server.

**Example**:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

users = []

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    users.append(data)
    return jsonify({"message": "User added", "user": data}), 201

if __name__ == "__main__":
    app.run(debug=True)
```

- **Request**:
  ```json
  {
      "id": 1,
      "name": "Alice"
  }
  ```

- **Response**:
  ```json
  {
      "message": "User added",
      "user": {"id": 1, "name": "Alice"}
  }
  ```

---

#### **PUT Request**

Update existing data.

**Example**:
```python
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    data = request.get_json()
    for user in users:
        if user["id"] == user_id:
            user.update(data)
            return jsonify({"message": "User updated", "user": user})
    return jsonify({"error": "User not found"}), 404
```

- **Request**:
  ```json
  {
      "name": "Alice Updated"
  }
  ```

- **Response**:
  ```json
  {
      "message": "User updated",
      "user": {"id": 1, "name": "Alice Updated"}
  }
  ```

---

#### **DELETE Request**

Remove data from the server.

**Example**:
```python
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    global users
    users = [user for user in users if user["id"] != user_id]
    return jsonify({"message": "User deleted"})
```

- **Response**:
  ```json
  {
      "message": "User deleted"
  }
  ```

---

### **3. Validating Input**

Use the `flask-marshmallow` or `pydantic` library for validating incoming data.

**Example with `pydantic`**:
```bash
pip install pydantic
```

**Code**:
```python
from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError

app = Flask(__name__)

class User(BaseModel):
    id: int
    name: str

@app.route("/users", methods=["POST"])
def add_user():
    try:
        data = User(**request.get_json())
        return jsonify({"message": "User added", "user": data.dict()}), 201
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

if __name__ == "__main__":
    app.run(debug=True)
```

---

### **4. Error Handling**

Handle errors gracefully using Flask's error handling.

**Example**:
```python
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404
```

---

### **5. Best Practices for REST API Development**

1. **Use Proper HTTP Status Codes**:
   - `200`: Success
   - `201`: Created
   - `400`: Bad Request
   - `404`: Not Found
   - `500`: Internal Server Error

2. **Validate Input**:
   - Ensure incoming data is in the correct format.

3. **Use JSON**:
   - Always use `jsonify()` to return data.

4. **Document the API**:
   - Use tools like Swagger or Postman to document endpoints.

5. **Secure the API**:
   - Implement authentication and rate limiting.

---

### **6. Example REST API Project**

Create a simple REST API to manage tasks.

**Endpoints**:
- `GET /tasks`: Retrieve all tasks.
- `POST /tasks`: Add a new task.
- `PUT /tasks/<id>`: Update a task.
- `DELETE /tasks/<id>`: Delete a task.

**Code**:
```python
from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    tasks.append(data)
    return jsonify({"message": "Task added", "task": data}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    for task in tasks:
        if task["id"] == task_id:
            task.update(data)
            return jsonify({"message": "Task updated", "task": task})
    return jsonify({"error": "Task not found"}), 404

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"})

if __name__ == "__main__":
    app.run(debug=True)
```

---


## **9. Object-Oriented Programming (OOP)**

---

#### **Introduction**

Object-Oriented Programming (OOP) is a programming paradigm based on the concept of objects, which are instances of classes. Python’s OOP capabilities allow you to create reusable, modular, and maintainable code by encapsulating data and behavior into objects.

---

### **1. Classes and Objects**

#### **Classes**

A class is a blueprint for creating objects. It defines attributes (data) and methods (functions) that the objects will have.

**Syntax**:
```python
class ClassName:
    # Constructor
    def __init__(self, attribute1, attribute2):
        self.attribute1 = attribute1
        self.attribute2 = attribute2
    
    # Method
    def method_name(self):
        # Code block
```

**Example**:
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi, I'm {self.name} and I'm {self.age} years old."

# Creating an object
p = Person("Alice", 30)
print(p.greet())
```

**Output**:
```plaintext
Hi, I'm Alice and I'm 30 years old.
```

---

#### **Objects**

An object is an instance of a class. You can create multiple objects from a single class.

**Example**:
```python
p1 = Person("Alice", 30)
p2 = Person("Bob", 25)

print(p1.greet())  # Hi, I'm Alice and I'm 30 years old.
print(p2.greet())  # Hi, I'm Bob and I'm 25 years old.
```

---

### **2. Attributes and Methods**

#### **Attributes**

Attributes are variables that belong to a class or an object. They can be defined in the constructor (`__init__`).

**Example**:
```python
class Car:
    def __init__(self, make, model):
        self.make = make
        self.model = model

car = Car("Toyota", "Corolla")
print(car.make)  # Toyota
print(car.model)  # Corolla
```

---

#### **Methods**

Methods are functions defined within a class. They operate on the attributes of the object.

**Example**:
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

rect = Rectangle(5, 10)
print(rect.area())  # 50
```

---

### **3. Inheritance**

Inheritance allows a class (child class) to inherit attributes and methods from another class (parent class).

**Example**:
```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def speak(self):
        return f"{self.name} barks."

dog = Dog("Buddy")
print(dog.speak())  # Buddy barks.
```

---

### **4. Encapsulation**

Encapsulation restricts direct access to certain attributes and methods, providing control over how data is accessed or modified.

1. **Public Attributes**:
   - Accessible from anywhere.
   - Example:
     ```python
     class Person:
         def __init__(self, name):
             self.name = name

     p = Person("Alice")
     print(p.name)  # Alice
     ```

2. **Private Attributes**:
   - Prefixed with `__` to make them private.
   - Example:
     ```python
     class Person:
         def __init__(self, name):
             self.__name = name

         def get_name(self):
             return self.__name

     p = Person("Alice")
     print(p.get_name())  # Alice
     ```

---

### **5. Polymorphism**

Polymorphism allows methods in different classes to have the same name but behave differently based on the object.

**Example**:
```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Bark!"

class Cat(Animal):
    def speak(self):
        return "Meow!"

animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())
```

**Output**:
```plaintext
Bark!
Meow!
```

---

### **6. Abstraction**

Abstraction hides implementation details and shows only the functionality. It can be achieved using abstract base classes (ABC).

**Example**:
```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14 * self.radius ** 2

circle = Circle(5)
print(circle.area())  # 78.5
```

---

### **7. Best Practices for OOP**

1. **Use Meaningful Class Names**:
   - Class names should describe their purpose (e.g., `Person`, `Rectangle`).

2. **Follow the DRY Principle**:
   - Avoid duplicating code by using inheritance or reusable methods.

3. **Use Encapsulation**:
   - Make attributes private when needed and provide getter/setter methods.

4. **Keep Classes Focused**:
   - A class should have a single responsibility.

5. **Use Abstraction and Polymorphism**:
   - Implement abstract base classes and override methods in child classes for flexible designs.

---