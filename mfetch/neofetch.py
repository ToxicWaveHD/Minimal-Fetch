from os.path import expanduser
import os
from mfetch.get_info import get_info
from mfetch.cimage import cimage
import click
from mfetch.get_info import run_command
from mfetch.get_info import run_command
from mfetch.get_info import get_info


@click.command()
def main():

    path = run_command("pip show mfetch | grep Location").split(": ")[1]

    from os.path import expanduser, exists, join

    # Load system info
    sysinfo = get_info()

    # === Load user preferences ===
    pref = {}
    home_config = join(expanduser("~"), ".config/mfetch/options")
    fallback_config = join(path, "mfetch/options")

    try:
        with open(home_config) as f:
            pref_lines = f.read().splitlines()
    except FileNotFoundError:
        with open(fallback_config) as f:
            pref_lines = f.read().splitlines()

    for line in pref_lines:
        if " " in line:
            var, val = line.split(" ", 1)
            pref[var] = val

    # === Apply preferences ===
    colon_padding = int(pref.get("text_spacer_size", 2))
    logo_padding = int(pref.get("logo_padding", 1))
    split_symb = (
        f"\\e[2m{pref['split_symbol']}\\e[0m"
        if pref.get("split_symbol") != "null"
        else " "
    )
    big = pref.get("logo_big") == "True"
    oslogo = (
        pref["os_logo"]
        if pref.get("os_logo") != "null"
        else sysinfo["os"].lower().split(" ")[0]
    )

    # === Load logo and color ===
    logof = "logo-big" if big else "logo"
    passfile = join(path, "mfetch", "logos", oslogo, logof)

    # Fallback to generic Linux logo if needed
    if not exists(passfile + ".png"):
        passfile = join(path, "mfetch", "logos", "linux", logof)

    cimage(passfile)

    with open(join(expanduser("~"), ".cache/mfetch/currentlogo")) as f:
        logo = f.read()

    with open(join(path, "mfetch/colour/colours")) as f:
        colours = f.read().replace("\n", "")

    # === Load additional logo metadata ===
    dat = {}
    try:
        dat_file = join(path, "mfetch", "logos", oslogo, "dat")
        with open(dat_file) as f:
            dat_lines = f.read().splitlines()
    except FileNotFoundError:
        with open(join(path, "mfetch", "logos", "linux", "dat")) as f:
            dat_lines = f.read().splitlines()

    for line in dat_lines:
        if ": " in line:
            var, val = line.split(": ", 1)
            dat[var] = val

    # === Formatting constants ===
    logo_col = f"\\e[3{dat.get('col', '7')}m"
    terminator = "\\e[0m"
    bold = "\\e[1m"
    split = ":" + " " * colon_padding

    def render_info(title, item):
        title = str(title)
        item = str(item)
        padding = " " * (maximum_title_size - len(title))
        return "".join(
            [
                bold,
                logo_col,
                title,
                terminator,
                split_symb,
                " " * colon_padding,
                padding,
                item,
            ]
        )

    maximum_title_size = 9

    # Define the base info keys
    info_keys = [
        ("OS", sysinfo["os"]),
        ("WM", sysinfo["wm"]),
        ("Kernel", sysinfo["kernel"]),
        ("Pkgs", sysinfo["packages"]),
        ("CPU", sysinfo["cpu"]),
        ("GPU", sysinfo["gpu"]),
    ]

    # Conditionally append GPU2
    if sysinfo.get("gpu2"):
        info_keys.append(("GPU2", sysinfo["gpu2"]))

    # Add memory as final stat
    info_keys.append(("Memory", sysinfo["memory"]))

    # Build final output lines
    line = [""]
    line += [render_info(k, v) for k, v in info_keys[:2]]
    line.append("")
    line += [render_info(k, v) for k, v in info_keys[2:]]
    line.append("")
    line.append(colours)

    out = []
    on = 0
    out.append("")
    lines = logo.split("\n")
    for on, i in enumerate(lines):
        g = line[on] if on < len(line) else ""
        out.append(f"{i}{' ' * logo_padding}{g}")

    os.system("echo -e '" + "\n".join(out) + "'")

    pass


if __name__ == "__main__":
    main()
