import os

# tool for getting system information by returning the output of a command


def get(thing):
    th = str(thing)
    tmp = os.popen(th).read()
    return tmp


def verify(package):
    found = True
    try:
        get(str("whereis " + package)).split(": ")[1]
    except:
        found = False

    return found


def find_gpu():
    gpu = get("lspci -v").split("00:02.0 VGA compatible controller: ")[1]
    gpu = gpu.split(" (")[0]

    fancy_gpu = (
        gpu.replace("Intel Corporation ", "")
        .replace(" Integrated Graphics Controller", "")
        .replace("Core Processor ", "")
    )

    return fancy_gpu


# find the OS
def find_os():
    try:
        os = open("/etc/os-release").read().split('PRETTY_NAME="')[1]
        os = os.split('"')[0]
    except:
        try:
            os = open("/etc/os-release").read().split('NAME="')[1]
            os = os.split('"')[0]
        except:
            try:
                os = open("/usr/os-release").read().split('PRETTY_NAME="')[1]
                os = os.split('"')[0]
            except:
                os = open("/usr/os-release").read().split('NAME="')[1]
                os = os.split('"')[0]
    return os


# find the CPU
def find_cpu():
    cpu = open("/proc/cpuinfo").read().split("\n")[4]
    cpu = cpu.split(": ")[1]

    fancy_cpu = cpu.split(" CPU")[0]  # remove the "cpu @ 0.00hz" part

    # some customizations to make the intel i series look cleaner after all this is minimal fetch
    if fancy_cpu.split(" ")[0] == "Intel(R)":
        fancy_cpu = fancy_cpu.split("Intel(R) Core(TM) ")[
            1
        ]  # removes the branding part that nobody cares about

    return fancy_cpu  # you can change "fancy_cpu" to "cpu" to avoid breakages and show full default cpu info


# Find the WM name
def find_wm():
    wm = get("wmctrl -m").split("\n")[0]
    wm = wm.split(": ")[1]
    return wm


def find_kern():
    kern = get("uname -r").split("\n")[
        0
    ]  # the .split part removes the newline at the end
    return kern


def find_memory():
    mem = get("free -m").split("\n")[1]
    total_mem = int(
        int(mem.split()[1]) / 100
    )  #  The double int is used to serve as a truncate
    used_mem = int(
        int(mem.split()[2]) / 100
    )  #   The double int is used to serve as a truncate

    total_mem = total_mem / 10  #  this makes it gigabytes rather than megabytes
    used_mem = used_mem / 10  #   this makes it gigabytes rather than megabytes

    ret = str(str(used_mem) + " / " + str(total_mem))
    ret = ret + " GB"  # Simple indicator
    return ret


def find_packages():

    packages = []

    try:
        if verify("pacman"):
            pacman_amount = len(get("pacman -Q").split("\n")) - 1

            if pacman_amount > 0:
                packages.append(str("pacman " + str(pacman_amount)))
    except:
        False

    try:
        if verify("flatpak"):
            flatpak_amount = len(get("flatpak list").split("\n")) - 1

            if flatpak_amount > 0:
                packages.append(str("flatpak " + str(flatpak_amount)))

    except:
        False
    try:
        if verify("dpkg"):
            dpkg_amount = len(get("dpkg-query -l").split("\n")) - 1

            if dpkg_amount > 0:
                packages.append(str("dpkg " + str(dpkg_amount)))
    except:
        False

    try:
        if verify("rpm"):
            rpm_amount = len(get("rpm -qa").split("\n")) - 1

            if rpm_amount > 0:
                packages.append(str("rpm " + str(rpm_amount)))
    except:
        False

    try:
        if verify("apk"):
            apk_amount = len(get("apk list --installed").split("\n")) - 1

            if apk_amount > 0:
                packages.append(str("apk " + str(apk_amount)))
    except:
        False

    # LOOKING TO COMMIT SOME CODE?
    # Add your distros pakcage manager with
    #
    # try:
    #  if verify(" <package manager command> "):
    #    pak_amount = len(get(" <package manager list installed command> ").split("\n"))-1
    #
    #    if pak_amount > 0:
    #      packages.append(str("<package manger name> " + str(pak_amount)))
    # except: False

    return " & ".join(packages)


sysinfo = {}

try:
    sysinfo["wm"] = find_wm()
except:
    sysinfo["wm"] = "null"

try:
    sysinfo["os"] = find_os()
except:
    sysinfo["os"] = "null"

try:
    sysinfo["cpu"] = find_cpu()
except:
    sysinfo["cpu"] = "null"

try:
    sysinfo["memory"] = find_memory()
except:
    sysinfo["memory"] = "null"

try:
    sysinfo["kernel"] = find_kern()
except:
    sysinfo["kernel"] = "null"

try:
    sysinfo["packages"] = find_packages()
except:
    sysinfo["packages"] = "null"

try:
    sysinfo["gpu"] = find_gpu()
except:
    sysinfo["gpu"] = "null"
