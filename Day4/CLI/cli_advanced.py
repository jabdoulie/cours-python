import argparse

parser = argparse.ArgumentParser(description="A CLI tool with error handling")
parser.add_argument("--age", type=int, help="Enter your age")
subparsers = parser.add_subparsers(dest="command")


args = parser.parse_args()
if args.command is None:
    parser.error("You must specify a subcommand.")
if args.age is not None and args.age < 0:
    parser.error("Age cannot be negative!")

print(f"Your age is: {args.age}")