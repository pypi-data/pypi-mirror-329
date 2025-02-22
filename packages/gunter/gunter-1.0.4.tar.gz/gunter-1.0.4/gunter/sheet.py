import argparse
from PIL import Image
from gunter.util import process_image

def main(*args):
    parser = argparse.ArgumentParser(description="GTRSheet - Convert a gridded image into a .gtr")
    parser.add_argument("-i", "--input", help="Path to the input file", required=True)
    parser.add_argument("-x", "--width", help="Width of a cell", type=int, required=True)
    parser.add_argument("-y", "--height", help="Height of a cell", type=int, required=True)
    parser.add_argument("-o", "--output", help="Path to the output file", required=True)

    args = parser.parse_args(args)
    
    q = Image.open(args.input).convert('RGB')
    
    out = "\n".join(process_image(q, args.width, args.height))        
    with open(args.output, "w+", encoding="utf-8") as o:
        o.write(out)

if __name__ == "__main__":
    import sys
    main(*sys.argv[1:])