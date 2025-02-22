import sys
import argparse
from . import sheet, draw, index, merge, to_bdf

__version__ = "1.0.3"

def main():
    parser = argparse.ArgumentParser(prog="gunter", description="Gunter: Program to turn any image of glyphs into a .hex-like format, and that into a .bdf")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    commands = {
        "sheet": sheet.main,
        "draw": draw.main,
        "index": index.main,
        "merge": merge.main,
        "to_bdf": to_bdf.main
    }
    
    for cmd in commands:
        subparsers.add_parser(cmd, help=f"Run {cmd} command")

    args, unknown_args = parser.parse_known_args()
    
    if args.command in commands:
        commands[args.command](*unknown_args)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()