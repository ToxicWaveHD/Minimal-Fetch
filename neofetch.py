import os, platform, subprocess, re, psutil
import socket
import __main__
from os.path import expanduser


def get(thing):
    th = str("neofetch" + " " + thing)
    tmp = (os.popen(th).read().replace("\n", "")).split(": ")[1]
    return tmp


pref = {}
pref_ = open(str(expanduser("~")) + "/.config/mfetch/options").read().split("\n")
for pref_itm in pref_:
    try:
        var, val = pref_itm.split(" ")
        pref.update({var: val})
    except:
        False

colon_padding = int(pref["text_spacer_size"])
logo_padding = int(pref["logo_padding"])

if not pref["split_symbol"] == "null":
    split_symb = pref["split_symbol"]
else:
    split_symb = " "

big = pref["logo_big"] == "True"
redact_ip = pref["hide_ip"] == "True"

# os.system('python3 cimage.py')
# passfile = 'colour/colours'
# exec(open("cimage.py").read())

if not pref["os_logo"] == "null":
    oslogo = pref["os_logo"]
else:
    oslogo = get("distro").lower().split(" ")[0]

if big:
    logof = "logo-big"
else:
    logof = "logo"
passfile = "logos/" + oslogo + "/" + logof
try:
    open(str(passfile + ".png"))
except:
    passfile = "logos/linux/" + logof
exec(open("cimage.py").read())

logo = str(open(str(expanduser("~")) + "/.cache/mfetch/currentlogo").read())
colours = str(open("colour/colours").read().replace("\n", ""))


def packages():
    pkgs = []
    for i in get("packages").split(", "):
        i = i.replace("(", "").replace(")", "")
        i = i.split(" ")
        pkgs.append(str(i[1] + " " + i[0]))
    return " & ".join(pkgs)


def get_system_info():
    system_info = {}
    system_info["OS"] = get("distro").replace("x86_64", "")

    cpu = get("cpu").split(" ")
    if cpu[0] == "Intel":
        system_info["CPU"] = cpu[1]
    else:
        system_info["CPU"] = " ".join(cpu)

    system_info["GPU"] = get("gpu")
    system_info["Pkgs"] = packages()
    system_info["Memory"] = get("memory")
    system_info["Kernel"] = get("kernel")

    return system_info


system_info = get_system_info()

line = ["", "OS", "", "Kernel", "Pkgs", "", "CPU", "GPU", "Memory", "", "Colours"]

dat = {}
dat_ = open("logos/" + oslogo + "/dat").read().split("\n")
for pref_itm in dat_:
    try:
        var, val = pref_itm.split(": ")
        dat.update({var: val})
    except:
        False

cols = []
cols.append(dat["col"])

out = []
on = 0
out.append("")
for i in logo.split("\n"):
    try:
        col = cols[(on % (len(cols)))]
        leng = (6) - (len(line[on]))
        if line[on] == "Colours":
            g = colours
        else:
            g = ("\\e[1m\\e[3"+col+"m"+str(line[on])+"\\e[0m"+split_symb+(" " * (leng + colon_padding))+str(system_info[line[on]]))
    except:
        g = " "
    on += 1
    out.append(str(i) + " " * logo_padding + str(g))

os.system("echo -e '" + "\n".join(out) + "'")
