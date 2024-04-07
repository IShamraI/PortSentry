#!/usr/bin/env python3

import sys
import argparse
from libs.knock import read_chain, executors


def main():
    """
    Main function.
    """
    parser = argparse.ArgumentParser(description="Knocking to the port")
    parser.add_argument("--chain", "-c", type=str, help="Input file with chain", default=None)

    args = parser.parse_args()

    if args.chain is None:
        print("No rules file specified.")
        sys.exit(1)

    print(f"Input file: {args.chain}")
    rules = read_chain(args.chain)

    for rule in rules:
        executors[rule['type']](**rule)


if __name__ == "__main__":
    main()
