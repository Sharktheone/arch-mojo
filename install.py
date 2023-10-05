import os
import shutil
import subprocess
import sys
import urllib.request

# TODO use shutil to copy files

arch = "x86_64-linux-gnu"


def param(name: str):
    try:
        return os.environ[name]
    except:
        return None


WORKING_DIR = "~/.local/arch-mojo/"
install_global = False
onlyMojo = False

for arg in sys.argv:
    if arg.startswith("--dir="):
        WORKING_DIR = arg.split("=")[1]
    elif arg.startswith("-d="):
        WORKING_DIR = arg.split("=")[1]
    elif arg == "--global":
        install_global = True
    elif arg == "-g":
        install_global = True
    elif arg == "--mojo":
        onlyMojo = True
    elif arg == "-m":
        onlyMojo = True
    elif arg == "--help" \
            or arg == "-h":
        print("Usage: python3 install.py [options]")
        print("Options:")
        print("  --dir=<path>  | -d=<path>  : Set the working directory")
        print("  --global      | -g         : Install the libs globally")
        print("  --help        | -h         : Show this help message")
        print("  --mojo        | -m         : Only install mojo (modular must be installed)")
        exit(0)

WORKING_DIR = WORKING_DIR.replace("~", param("HOME"))
if WORKING_DIR[-1] != "/":
    WORKING_DIR += "/"

modular = shutil.which("modular") is not None

authenticated = False
if modular:
    authenticated = "user.id" in subprocess.run(["modular", "config-list"], capture_output=True).stdout.decode("utf-8")

if onlyMojo and not modular:
    print("Modular must be installed to install mojo")
    exit(1)
if onlyMojo and not authenticated:
    print("You must be authenticated in modular to install mojo")
    exit(1)

try:
    os.makedirs(WORKING_DIR)
except FileExistsError:
    pass

# install modular if not installed
if not modular:
    # download PKGBUILD
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/PKGBUILD",
                               f"{WORKING_DIR}PKGBUILD")
    os.system(f"cd {WORKING_DIR} && makepkg -si")

# authenticate in modular
if not authenticated:
    token = input("Please enter your Modular auth token: ")
    os.system(f"modular auth {token}")

# download ncurses lib

urllib.request.urlretrieve("https://ftp.debian.org/debian/pool/main/n/ncurses/libncurses6_6.4-4_amd64.deb",
                           f"{WORKING_DIR}libncurses.deb")

urllib.request.urlretrieve("https://ftp.debian.org/debian/pool/main/libe/libedit/libedit2_3.1-20221030-2_amd64.deb",
                           f"{WORKING_DIR}libedit.deb")

os.system(f"cd {WORKING_DIR} && ar -vx libncurses.deb && tar -xf data.tar.xz")
os.system(f"cd {WORKING_DIR} && ar -vx libedit.deb && tar -xf data.tar.xz")

# copy libs
if install_global:
    os.system(f"sudo cp {WORKING_DIR}lib/{arch}/* /lib/")
    os.system(f"sudo cp {WORKING_DIR}usr/lib/{arch}/* /usr/lib/")
    os.system(f"sudo cp {WORKING_DIR}lib/{arch}/* /usr/lib/")
else:
    mojo_lib_path = "/home/$USER/.local/lib/mojo"

    os.system(f"mkdir -p {mojo_lib_path}")

    os.system(f"cp {WORKING_DIR}lib/{arch}/libncurses.so.6.4 {mojo_lib_path}/libncurses.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libform.so.6.4 {mojo_lib_path}/libform.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libpanel.so.6.4 {mojo_lib_path}/libpanel.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libedit.so.2.0.70 {mojo_lib_path}/libedit.so.2")

# install mojo
os.system("modular install mojo")


def rc_path():
    match param("SHELL").split("/")[-1]:
        case "bash":
            return f"{param('HOME')}/.bashrc"
        case "zsh":
            return f"{param('HOME')}/.zshrc"
        case _:
            path = input("Please enter the path to your shell rc file (e.g. ~/.bashrc for bash): ")
            return path.replace("~", param("HOME"))


rc_pth = rc_path()

rc_file = open(rc_pth, "a")
shell_rc = open(rc_pth, "r").read()

home = param("HOME")

# check if exports are already in rc file
if param("LD_LIBRARY_PATH") is None or \
        "~/.local/lib/mojo" not in param("LD_LIBRARY_PATH") \
        or f"{home}.local/lib/mojo" not in param("LD_LIBRARY_PATH"):
    rc_file.write("export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib/mojo\n")

if param("PATH") is None \
        or "~/.modular/pkg/packages.modular.com_mojo/bin/" not in param("PATH") \
        or f"{home}.modular/pkg/packages.modular.com_mojo/bin/" not in param("PATH"):
    rc_file.write("export PATH=$PATH:~/.modular/pkg/packages.modular.com_mojo/bin/\n")
rc_file.close()

# fix crashdb directory not found:
os.makedirs(f"{home}/.modular/crashdb", exist_ok=True)

print(f"Please restart your shell or run `source {rc_pth} `to complete the installation")
