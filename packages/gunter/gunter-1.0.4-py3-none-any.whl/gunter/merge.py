from gunter.util import merge
import argparse

def main(*args):
    parser = argparse.ArgumentParser(description="GTRMerge - Merge 2 GTR Files")
    parser.add_argument("-1", "--gtr1", help="Path to the first GTR file", required=True)
    parser.add_argument("-2", "--gtr2", help="Path to the second GTR file", required=True)
    parser.add_argument("-o", "--out", help="Path to the output file", required=True)

    args = parser.parse_args(args)
    
    with open(args.gtr1, "r", encoding="utf-8") as f:
        g = f.read().splitlines()
    with open(args.gtr2, "r", encoding="utf-8") as f:
        h = f.read().splitlines()

    out = "\n".join(merge(g, h))
    with open(args.out, "w+", encoding="utf-8") as f:
        f.write(out)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])