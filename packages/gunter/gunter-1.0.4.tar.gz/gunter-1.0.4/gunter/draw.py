from gunter.util import to_gtr, from_gtr
import argparse

def main(*args):
    parser = argparse.ArgumentParser(description="GTRDraw - Convert .txt into .gtr and back")
    parser.add_argument("mode", choices=["txt", "gtr"], help="Conversion mode")
    parser.add_argument("-i", "--input", required=True)

    args = parser.parse_args(args)
    
    if args.mode == "txt":
        with open(args.input, "r", encoding="utf-8") as f:
            q = f.read().splitlines()
        print(to_gtr(q))
    
    if args.mode == "gtr":
        print("\n".join(from_gtr(args.input)))

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])