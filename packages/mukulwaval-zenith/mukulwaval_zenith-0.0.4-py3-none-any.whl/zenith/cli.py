"""CLI interface for zenith project.

This module defines the entry point for the CLI.
It now accepts a command-line argument to customize the greeting.
"""

import argparse

from zenith.base import get_greeting


def main():  # pragma: no cover
    """
    The main function executes on commands:
    `python -m zenith` and `$ zenith`.

    It parses command-line arguments to optionally get a custom name,
    then prints a greeting message.
    """
    parser = argparse.ArgumentParser(
        description="Zenith CLI - Print a greeting message."
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        default="World",
        help="Name to greet (default: World)",
    )
    args = parser.parse_args()
    message = get_greeting(args.name)
    print(message)


if __name__ == "__main__":  # pragma: no cover
    main()
