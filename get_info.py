import os
import subprocess


def run_command(command):
    """
    Runs a shell command and returns the output as a string.
    """
    try:
        result = subprocess.check_output(command, shell=True, text=True)
        return result.strip()
    except subprocess.CalledProcessError:
        return ""


def verify(package):
    """
    Verifies if a package is installed on the system.
    """
    output = run_command(f"whereis {package}")
    return output.split(": ")[1] if output else False


def find_gpu():
    """
    Finds the GPU information.
    """
    output = run_command("lspci -v")
    gpu_info = output.split("00:02.0 VGA compatible controller: ")[1].split(" (")[0]
    return (
        gpu_info.replace("Intel Corporation ", "")
        .replace(" Integrated Graphics Controller", "")
        .replace("Core Processor ", "")
    )


def find_os():
    """
    Finds the operating system information.
    """
    try:
        with open("/etc/os-release") as file:
            os_info = file.read().split('PRETTY_NAME="')[1].split('"')[0]
    except FileNotFoundError:
        os_info = "Unknown"
    return os_info


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
    wm = run_command("wmctrl -m").split("\n")[0]
    wm = wm.split(": ")[1]
    return wm


def find_kern():
    kern = run_command("uname -r").split("\n")[
        0
    ]  # the .split part removes the newline at the end
    return kern


def find_memory():
    mem = run_command("free -m").split("\n")[1]
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
            pacman_amount = len(run_command("pacman -Q").split("\n")) - 1

            if pacman_amount > 0:
                packages.append(str("pacman " + str(pacman_amount)))
    except:
        False

    try:
        if verify("flatpak"):
            flatpak_amount = len(run_command("flatpak list").split("\n")) - 1

            if flatpak_amount > 0:
                packages.append(str("flatpak " + str(flatpak_amount)))

    except:
        False
    try:
        if verify("dpkg"):
            dpkg_amount = len(run_command("dpkg-query -l").split("\n")) - 1

            if dpkg_amount > 0:
                packages.append(str("dpkg " + str(dpkg_amount)))
    except:
        False

    try:
        if verify("rpm"):
            rpm_amount = len(run_command("rpm -qa").split("\n")) - 1

            if rpm_amount > 0:
                packages.append(str("rpm " + str(rpm_amount)))
    except:
        False

    try:
        if verify("apk"):
            apk_amount = len(run_command("apk list --installed").split("\n")) - 1

            if apk_amount > 0:
                packages.append(str("apk " + str(apk_amount)))
    except:
        False
    """
    
    LOOKING TO COMMIT SOME CODE?
    Add your distros pakcage manager with
    
    try:
     if verify(" <package manager command> "):
       pak_amount = len(run_command(" <package manager list installed command> ").split("\n"))-1
    
       if pak_amount > 0:
         packages.append(str("<package manger name> " + str(pak_amount)))
    except: False

    return " & ".join(packages)

    """


def get_info():
    """
    Retrieves system information and returns it as a dictionary.
    """
    sysinfo = {
        "wm": find_wm(),
        "os": find_os(),
        "cpu": find_cpu(),
        "memory": find_memory(),
        "kernel": find_kern(),
        "packages": find_packages(),
        "gpu": find_gpu(),
    }
    return sysinfo
