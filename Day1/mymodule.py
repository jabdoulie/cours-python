def multiply(a, b):
    return a * b


def add(x, y):
    return x + y

def subtract(x, y):
    return x - y


def sum_even_numbers(numbers):
    return sum([num for num in numbers if num % 2 == 0])


def read_file(filename):
    # Open the file in read mode
    with open(filename, 'r') as file:
        return file.read()
    
def write_file(filename, content):
    # Open the file in write mode
    with open(filename, 'w') as file:
        file.write(content) 