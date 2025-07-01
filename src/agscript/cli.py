import argparse
import subprocess


def main():
    parser = argparse.ArgumentParser(
        description="A simple command-line example package."
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all files in the current directory (runs 'ls -a').",
    )
    parser.add_argument(
        "name",
        nargs="*",
        default=[],
        help="An optional name to greet.",
    )

    args = parser.parse_args()

    print("from cli!")
    print(args)

    if args.list:
        subprocess.run(["ls", "-a"])

    if args.name:
        name_str = " ".join(args.name)
        print(f"Hello, {name_str}!")
    elif not args.list:
        # If no name was given and --list was not used, print the default message.
        print("Hello from agscript!")


if __name__ == "__main__":
    main()
