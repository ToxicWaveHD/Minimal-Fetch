import os
from PIL import Image

ech = 'echo -e "'
end = '\\e[0m"'
nul = "\\e[0m"

cols = [
    "\\e[30m",
    "\\e[40m",
    "\\e[31m",
    "\\e[41m",
    "\\e[32m",
    "\\e[42m",
    "\\e[33m",
    "\\e[43m",
    "\\e[34m",
    "\\e[44m",
    "\\e[35m",
    "\\e[45m",
    "\\e[36m",
    "\\e[46m",
    "\\e[37m",
    "\\e[47m",
]


def save(inputt):
    """
    Saves input to a file.
    """
    directory = os.path.expanduser("~/.cache/mfetch/")
    os.makedirs(directory, exist_ok=True)  # Create directory if it doesn't exist
    filee = os.path.join(directory, "currentlogo")
    with open(filee, "w") as fp:
        fp.write(str(inputt))


def colconv(col):
    """
    Converts RGBA color to ANSI color code.
    """
    r, g, b, a = col
    r = int((r / 255) + 0.5) != 0
    g = int((g / 255) + 0.5) != 0
    b = int((b / 255) + 0.5) != 0
    a = int((a / 255) + 0.5) != 0

    if a:
        if r & g & b:
            return "7"
        if g & b:
            return "6"
        if r & b:
            return "5"
        if r & g:
            return "3"
        if r:
            return "1"
        if g:
            return "2"
        if b:
            return "4"
        else:
            return "0"
    else:
        return " "


def col(col, mod):
    """
    Returns ANSI color escape sequences.
    """
    return cols[col * 2 + mod]


def blockrender(val0, val1):
    """
    Renders a block based on color values.
    """
    out = ""
    if val0 == " " and val1 == " ":
        out = " "
    else:
        if val0 != " ":
            if val1 != " ":
                col0 = col(int(val0), 0)
                col1 = col(int(val1), 1)
            else:
                col0 = col(int(val0), 0)
                col1 = ""
            out = col0 + col1 + "▀"
        else:
            col0 = nul
            col1 = col(int(val1), 0)
            out = col0 + col1 + "▄"
    return out + nul


def cimage(passfile):
    """
    Creates an ANSI art image from a PNG file.
    """
    output = []

    img = Image.open(passfile + ".png")
    width, height = img.size
    image = ""

    for y in range(height):
        for x in range(width):
            image = image + str(colconv(img.getpixel((x, y))))
        image = image + str("\n")

    ylength = max(len(line) for line in image.split("\n"))

    imagemod = [line.ljust(ylength) for line in image.split("\n")]
    image = "\n".join(imagemod)

    if not len(image.split("\n")) % 2 == 0:
        wdth = len(image.split("\n")[0])
        image = image + ("\n" + (" " * wdth))

    img = image.split("\n")
    ylen = len(img)

    for y in range(int(ylen / 2)):
        line0 = img[y * 2]
        line1 = img[y * 2 + 1]
        for x in range(len(line0)):
            output.append(str(blockrender(line0[x], line1[x])))
        if y != ylen / 2:
            output.append("\n")

    save(str("".join(output)))
