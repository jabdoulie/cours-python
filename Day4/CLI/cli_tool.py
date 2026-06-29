import argparse

def greet(name):
    print(f"Hello, {name}!")

def goodbye(name):
    print(f"Goodbye, {name}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A CLI tool with subcommands")
    subparsers = parser.add_subparsers(dest="command")  # Add subcommands

    # Subcommand: greet
    greet_parser = subparsers.add_parser("greet", help="Greet someone")
    greet_parser.add_argument("name", help="Person's name")

    # Subcommand: goodbye
    goodbye_parser = subparsers.add_parser("goodbye", help="Say goodbye to someone")
    goodbye_parser.add_argument("name", help="Person's name")

    args = parser.parse_args()

    if args.command == "greet":
        greet(args.name)
    elif args.command == "goodbye":
        goodbye(args.name)