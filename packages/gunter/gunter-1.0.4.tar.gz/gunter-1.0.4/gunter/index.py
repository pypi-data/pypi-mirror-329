from gunter.util import reindex
import argparse

def main(*args):
    parser = argparse.ArgumentParser(description="GTRIndex - Give a GTR a new index (for assigning codepoints)")
    parser.add_argument("-g", "--gtr", help="Path to the GTR file", required=True)
    parser.add_argument("-c", "--char", help="Path to the file containing the characters", required=True)
    parser.add_argument("-o", "--out", help="Path to the output file", required=True)

    args = parser.parse_args(args)
    
    with open(args.gtr, "r", encoding="utf-8") as f:
        g = f.read().splitlines()
    with open(args.char, "r", encoding="utf-8") as f:
        c = f.read()

    out = "\n".join(reindex(g, c))
    with open(args.out, "w+", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])