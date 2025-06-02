import re
import subprocess
import shutil


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
    return shutil.which(package) is not None


# def verify(package):
#    """
#    Verifies if a package is installed on the system.
#    """
#    try:
#      open("/bin/" + package)
#      output = True
#    except:
#      output = False
#
#
#    return output


def is_wsl():
    """
    Checks if the script is running in a WSL environment.
    """
    return (
        "microsoft-standard" in run_command("uname -r").lower()
        or "wsl" in run_command("uname -r").lower()
    )


def find_gpu():
    """
    Finds the GPU information.
    """
    if is_wsl():
        try:
            command = 'powershell.exe "Get-CimInstance Win32_VideoController | Select-Object -ExpandProperty Name"'
            output = run_command(command)
            if output:
                return output.split("\n")
            else:
                return "None found in WSL"
        except:
            return "None found in WSL"
    if verify("lspci"):
        try:
            output = run_command("lspci -v")
            gpu_info = output.split("00:02.0 VGA compatible controller: ")[1].split(
                " ("
            )[0]
            return (
                gpu_info.replace("Intel Corporation ", "")
                .replace(" Integrated Graphics Controller", "")
                .replace("Core Processor ", "")
            )
        except:
            return "None found"
    else:
        return "NEEDS DEPENDENCY 'lspci'"


def find_os():
    try:
        with open("/etc/os-release") as file:
            content = file.read()
            match = re.search(r'PRETTY_NAME="([^"]+)"', content)
            return match.group(1) if match else "Unknown"
    except FileNotFoundError:
        return "Unknown"


# find the CPU
def find_cpu():
    try:
        cpu = open("/proc/cpuinfo").read().split("\n")[4]
        cpu = cpu.split(": ")[1]

        fancy_cpu = cpu.split(" CPU")[0]  # remove the "cpu @ 0.00hz" part

        # some customizations to make the intel i series look cleaner after all this is minimal fetch
        if fancy_cpu.split(" ")[0] == "Intel(R)":
            fancy_cpu = fancy_cpu.split("Intel(R) Core(TM) ")[
                1
            ]  # removes the branding part that nobody cares about

        return fancy_cpu  # you can change "fancy_cpu" to "cpu" to avoid breakages and show full default cpu info
    except:
        return "cpu not found"


# Find the WM name
def find_wm():
    try:
        wm = run_command("echo $XDG_CURRENT_DESKTOP")
        if wm == "":
            try:
                if verify("wmctrl"):
                    wm = run_command("wmctrl -m")
                    wm = wm.split("Name: ")[1]
                    wm = wm.split("\n")[0]
            except:
                wm = "Unknown"
    except:
        wm = "Unknown"
    return wm


def find_kern():
    kern = run_command("uname -r").split("\n")[
        0
    ]  # the .split part removes the newline at the end
    return kern


def find_memory():
    mem = run_command("free -m").split("\n")[1]
    total_mem = int(
        int(mem.split()[1]) / 10
    )  #  The double int is used to serve as a truncate
    used_mem = int(
        int(mem.split()[2]) / 10
    )  #   The double int is used to serve as a truncate

    total_mem = total_mem / 100  #  this makes it gigabytes rather than megabytes
    used_mem = used_mem / 100  #   this makes it gigabytes rather than megabytes

    ret = str(str(used_mem) + "\\e[2m / \\e[0m" + str(total_mem))
    ret = ret + " GB"  # Simple indicator
    return ret


def find_packages():
    packages = []

    managers = [
        ("pacman", "pacman -Q"),
        ("flatpak", "flatpak list"),
        ("pip", "pip list"),
        ("dpkg", "dpkg-query -l"),
        ("rpm", "rpm -qa"),
        ("apk", "apk list --installed"),
    ]

    for name, command in managers:
        if verify(name):
            try:
                output = run_command(command)
                count = len([line for line in output.splitlines() if line.strip()])
                if count > 0:
                    packages.append(f"{name} {count}")
            except:
                continue

    return " \033[2m&\033[0m ".join(packages)


def get_info():
    """
    Retrieves system information and returns it as a dictionary.
    """
    gpu_1 = None
    gpu_2 = None
    gpu = find_gpu()
    if len(gpu) > 1:
        gpu_1 = gpu[0]
        gpu_2 = gpu[1]

    sysinfo = {
        "wm": find_wm(),
        "os": find_os(),
        "cpu": find_cpu(),
        "memory": find_memory(),
        "kernel": find_kern(),
        "packages": find_packages(),
        "gpu": gpu_1 if gpu_1 else "None",
        "gpu2": gpu_2 if gpu_2 else None,
    }
    return sysinfo


get_info()
