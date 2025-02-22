from gunter.util import compile_font
import argparse
import json

def main(*args):
    parser = argparse.ArgumentParser(description="GTR2BDF - Convert .gtr into a .bdf font alongside a JSON of properties")
    parser.add_argument("-i", "--input", help="Path to the input file", required=True)
    parser.add_argument("-j", "--json", help="Path to the JSON file", required=True)
    parser.add_argument("-o", "--output", help="Path to the output file", required=True)

    args = parser.parse_args(args)
    
    with open(args.input, "r", encoding="utf-8") as f:
        q = f.read().splitlines()
    with open(args.json, "r", encoding="utf-8") as f:
        j = json.load(f)

    out = compile_font(q, j)

    with open(args.output, "w+", encoding="utf-8") as o:
        o.write(out)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])