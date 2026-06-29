import concurrent.futures

def process_file(file):
    print(f"Processing {file}")

files = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt", "file6.txt"]

with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(process_file, files)