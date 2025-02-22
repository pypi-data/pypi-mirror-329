import math
import re

def byte_padding(n):
    byte = math.ceil(len(n)/8)*8
    return n + "0"*(byte-len(n))

def n_split(n, s):
    return re.findall("."*s, n)

def to_gtr(s):
    width = max([len(l) for l in s])
    bittext = [byte_padding(l.replace("-", "0").replace("#", "1")[::-1].zfill(width)[::-1]) for l in s]
    return format(width, "x").upper() + "/" + "".join([format(int(bit, 2), "x").zfill(math.ceil(width/8)*2) for bit in bittext]).upper()

def from_gtr(s):
    width, byte = s.split("/")
    width = int(width, 16)
    bw = math.ceil(width/8)*2
    img = []
    for h in n_split(byte, bw):
        q = "".join(format(int(h, 16), "b").zfill(4)).zfill(bw*4)[:width]
        img.append(q.replace("0", "-").replace("1", "#"))
    return img

def reindex(g, c):
    c = list(c)
    gtr = []
    for q,k in zip(g, c, strict=True):
        _, width, bytetext, *_ = q.split("/")
        point = format(ord(k), "x").upper().zfill(2)
        gtr.append(("/".join((point, width, bytetext)), k))
    gtr = [x[0] for x in sorted(gtr, key=lambda z: z[1])]
    return gtr

def merge(g, h):
    indexes = []
    gtr = []
    for cg in g:
        cg = cg.split("/")
        if cg[0] in indexes:
            raise Exception
        gtr.append((cg[0], f"{cg[1]}/{cg[2]}"))
        indexes.append(cg[0])
    for ch in h:
        ch = ch.split("/")
        if ch[0] in indexes:
            raise Exception
        gtr.append((ch[0], f"{ch[1]}/{ch[2]}"))
        indexes.append(ch[0])
    return ["/".join(x) for x in sorted(gtr, key=lambda z: int(z[0], 16))]

def process_image(img, cw, ch):
    iw, ih = img.size
    index = 0
    gtr = []
    for y in range(0, ih, ch):
        for x in range(0, iw, cw):
            px = map(lambda z: "#" if z == (0,0,0) else "-", list(img.crop((x, y, x + cw, y + ch)).getdata()))
            px = n_split("".join(px), cw)
            px = to_gtr(px)
            if (px.split("/")[1].replace("0", "") == "") and ((x, y) != (0, 0)):
                break
            gtr.append(f"{format(index, 'x').upper()}/{px}")
            index += 1
    return gtr

def compile_font(bytetext, json):
    bdf = "STARTFONT 2.1\n"
    prop = [
        f'FONT_VERSION "{json.get("version", "1.0.0")}"',
        'FONT_TYPE "Bitmap"',
        f'FOUNDRY "{json.get("foundry", "author")}"',
        f'FAMILY_NAME "{json.get("family_name", "default")}"',
        f'SLANT "{json.get("slant", "R")}"',
        f'WEIGHT_NAME "{json.get("weight_name", "medium")}"',
        f'PIXEL_SIZE {json.get("pixel_size", 16)}',
        f'RESOLUTION_X {json.get("resolution_x", 75)}',
        f'RESOLUTION_Y {json.get("resolution_y", 75)}',
        'SPACING "C"',
        f'AVERAGE_WIDTH {json.get("average_width", 80)}',
        f'CHARSET_REGISTRY "{json.get("charset_registry", "ISO10646")}"',
        f'CHARSET_ENCODING "{json.get("charset_encoding", "1")}"',
        f'X_HEIGHT {json.get("x_height", 8)}',
        f'FONT_ASCENT {json.get("font_ascent", 14)}',
        f'FONT_DESCENT {json.get("font_descent", 2)}',
        f'DEFAULT_CHAR {json.get("default_char", 32)}',
    ]
    avgwidth = json.get("average_width", 80)
    height = json.get("font_ascent", 14) + json.get("font_descent", 2)
    props = lambda z: prop[z].split(" ")[1].replace('"', "")
    bdf += "\n".join([
        f"FONT -{'-'.join([props(i) for i in [2, 3, 4, 5]])}-normal--{'-'.join([props(i) for i in [6, 7, 8, 9, 10, 11, 12, 13]])}",
        "COMMENT Created via GUNTER, by @saperoi at www.icosahedr.online",
        "COMMENT GUNTER Source Code available at https://git.icosahedr.online/sapero/gunter",
        f"SIZE {' '.join([props(i) for i in [6, 7, 8]])}",
        f"FONTBOUNDINGBOX {avgwidth//10} {props(6)} 0 -{props(-2)}",
        f"STARTPROPERTIES {len(prop)}",
        *prop,
        "ENDPROPERTIES",
        f"CHARS {len(bytetext)}",
        ""
    ])
    rightmargin = json.get("right_margin", 0)
    for gtr in bytetext:
        point, width, byte, *_ = gtr.split("/")
        width = int(width, 16)
        bdf += "\n".join([
            f"STARTCHAR U+{point.zfill(4)}",
            f"ENCODING {int(point, 16)}",
            f"SWIDTH {(1000*width)//height} 0",
            f"DWIDTH {width+rightmargin} 0",
            f"BBX {width} {height} 0 -{props(-2)}",
            "BITMAP",
            *n_split(byte, math.ceil(width/8)*2),
            "ENDCHAR",
            ""
        ])

    bdf += "ENDFONT"
    return bdf