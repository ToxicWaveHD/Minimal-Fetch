import os
from PIL import Image

ECH = 'echo -e "'
END = '\\e[0m"'
NUL = "\\e[0m"

# ANSI color codes: index pairs correspond to foreground and background color codes
COLS = [
    "\\e[30m",
    "\\e[40m",  # black fg/bg
    "\\e[31m",
    "\\e[41m",  # red
    "\\e[32m",
    "\\e[42m",  # green
    "\\e[33m",
    "\\e[43m",  # yellow
    "\\e[34m",
    "\\e[44m",  # blue
    "\\e[35m",
    "\\e[45m",  # magenta
    "\\e[36m",
    "\\e[46m",  # cyan
    "\\e[37m",
    "\\e[47m",  # white
]


def save(content):
    """
    Saves content string to ~/.cache/mfetch/currentlogo, creating directories if needed.
    """
    directory = os.path.expanduser("~/.cache/mfetch/")
    os.makedirs(directory, exist_ok=True)
    filepath = os.path.join(directory, "currentlogo")
    with open(filepath, "w") as f:
        f.write(str(content))


def colconv(rgba):
    """
    Convert an RGBA tuple to a simplified ANSI color index (0-7) or ' ' for transparent.
    Uses a bitmask approach for red, green, blue channels presence.
    """
    r, g, b, a = rgba
    if a < 128:
        return " "
    # Normalize to binary presence
    r_bit = 1 if r > 127 else 0
    g_bit = 1 if g > 127 else 0
    b_bit = 1 if b > 127 else 0

    # Compose color index according to bits (rough approximation)
    if r_bit and g_bit and b_bit:
        return "7"  # white
    if g_bit and b_bit:
        return "6"  # cyan
    if r_bit and b_bit:
        return "5"  # magenta
    if r_bit and g_bit:
        return "3"  # yellow
    if r_bit:
        return "1"  # red
    if g_bit:
        return "2"  # green
    if b_bit:
        return "4"  # blue
    return "0"  # black


def col(color_idx, mod):
    """
    Return ANSI escape sequence for color index with mod (0=fg,1=bg).
    """
    idx = int(color_idx) * 2 + mod
    return COLS[idx]


def blockrender(val0, val1):
    """
    Render a combined block character based on two ANSI color codes.
    Uses '▀' (upper half block) and '▄' (lower half block).
    """
    if val0 == " " and val1 == " ":
        return " "
    if val0 != " ":
        col0 = col(val0, 0)
        col1 = col(val1, 1) if val1 != " " else ""
        return f"{col0}{col1}▀{NUL}"
    else:
        col0 = NUL
        col1 = col(val1, 0)
        return f"{col0}{col1}▄{NUL}"


def cimage(filename):
    """
    Convert a PNG image to ANSI art using half-block characters.
    Saves output to ~/.cache/mfetch/currentlogo.
    """
    img = Image.open(f"{filename}.png").convert("RGBA")
    width, height = img.size

    # Convert each pixel to ANSI color index string lines
    lines = []
    for y in range(height):
        line = "".join(colconv(img.getpixel((x, y))) for x in range(width))
        lines.append(line)

    # Pad lines to equal length
    max_len = max(len(line) for line in lines)
    lines = [line.ljust(max_len) for line in lines]

    # Make sure number of lines is even (for pairing rows)
    if len(lines) % 2 != 0:
        lines.append(" " * max_len)

    output = []
    for y in range(0, len(lines), 2):
        line0 = lines[y]
        line1 = lines[y + 1]
        for x in range(max_len):
            output.append(blockrender(line0[x], line1[x]))
        if y + 2 < len(lines):
            output.append("\n")

    save("".join(output))
