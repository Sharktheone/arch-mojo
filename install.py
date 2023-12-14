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


home = param("HOME")
if home is None:
    home = "~"

WORKING_DIR = "~/.local/arch-mojo/"
install_global = False
onlyMojo = False
fedora = False
mojo_lib_path_from_home = ".local/lib/mojo"
mojo_lib_path = f"{home}/{mojo_lib_path_from_home}"
skip_next_arg = False
token = None
modular = shutil.which("modular") is not None

authenticated = False
# if modular:
#     authenticated = "user.id" in subprocess.run(["modular", "config-list"], capture_output=True).stdout.decode("utf-8")

for arg in sys.argv:
    if skip_next_arg:
        skip_next_arg = False
        continue

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
    elif arg == "--fedora":
        fedora = True
    elif arg == "-f":
        fedora = True
    elif arg == "--modular-token":
        index = sys.argv.index(arg) + 1
        if index >= len(sys.argv):
            print("No token provided")
            exit(1)
        token = sys.argv[index]

        if token == "" or not token.startswith("mut_") or not len(token) == 36:
            print("Invalid token")
            exit(1)
        skip_next_arg = True
    elif arg == "--help" \
            or arg == "-h":
        print("Usage: python3 install.py [options]")
        print("Options:")
        print("  --dir=<path>  | -d=<path>  : Set the working directory")
        print("  --global      | -g         : Install the libs globally")
        print("  --help        | -h         : Show this help message")
        print("  --mojo        | -m         : Only install mojo (modular must be installed)")
        print("  --fedora      | -f         : Install for fedora")
        print("  --modular-token <token>    : Set the modular token")
        exit(0)

WORKING_DIR = WORKING_DIR.replace("~", param("HOME"))
if WORKING_DIR[-1] != "/":
    WORKING_DIR += "/"

if onlyMojo and not modular:
    print("Modular must be installed to install mojo")
    exit(1)

try:
    os.makedirs(WORKING_DIR)
except FileExistsError:
    pass

if fedora:
    os.system("sudo dnf install binutils")

    urllib.request.urlretrieve("http://ftp.debian.org/debian/pool/main/n/ncurses/libtinfo6_6.4-4_amd64.deb",
                               f"{WORKING_DIR}libtinfo.deb")
    os.system(f"cd {WORKING_DIR} && ar -vx libtinfo.deb && tar -xf data.tar.xz")
    if install_global:
        os.system(f"sudo cp {WORKING_DIR}lib/{arch}/* /usr/lib/")
    else:
        os.system(f"mkdir -p {mojo_lib_path}")

        os.system(f"cp {WORKING_DIR}lib/{arch}/libtinfo.so.6.4 {mojo_lib_path}/libtinfo.so.6")

# install modular if not installed
if not modular:
    # download PKGBUILD
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/PKGBUILD",
                               f"{WORKING_DIR}PKGBUILD")
    os.system(f"cd {WORKING_DIR} && makepkg -si")

# authenticate in modular
if not authenticated:
    if token is None:
        token = param("MODULAR_TOKEN")
    if token is None:
        token = input("Please enter your Modular auth token: ")
    os.system(f"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{mojo_lib_path} modular auth {token}")

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
    os.system(f"mkdir -p {mojo_lib_path}")

    os.system(f"cp {WORKING_DIR}lib/{arch}/libncurses.so.6.4 {mojo_lib_path}/libncurses.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libform.so.6.4 {mojo_lib_path}/libform.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libpanel.so.6.4 {mojo_lib_path}/libpanel.so.6")
    os.system(f"cp {WORKING_DIR}/usr/lib/{arch}/libedit.so.2.0.70 {mojo_lib_path}/libedit.so.2")

# install mojo
mojo = shutil.which(f"PATH=$PATH:{home}.modular/pkg/packages.modular.com_mojo/bin/ mojo") is not None
if mojo:
    print("Mojo is already installed... cleaning up")
    os.system(f"PATH=$PATH:{home}.modular/pkg/packages.modular.com_mojo/bin/ modular clean")

os.system(f"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{mojo_lib_path} modular install mojo")

# fix crashdb directory not found:
os.makedirs(f"{home}/.modular/crashdb", exist_ok=True)


def rc_path():
    match param("SHELL").split("/")[-1]:
        case "bash":
            return f"{param('HOME')}/.bashrc"
        case "zsh":
            return f"{param('HOME')}/.zshrc"
        case _:
            path = input(
                "Please enter the path to your shell rc file (e.g. ~/.bashrc for bash) or press ENTER to skip:")
            if path == "":
                return None
            return path.replace("~", param("HOME"))


rc_pth = rc_path()

if rc_pth is None:
    print("Skipping rc file installation")
    exit(0)

rc_file = open(rc_pth, "a")
shell_rc = open(rc_pth, "r").read()

# check if exports are already in rc file
if param("LD_LIBRARY_PATH") is None or \
        f"~/{mojo_lib_path_from_home}" not in param("LD_LIBRARY_PATH") \
        or mojo_lib_path not in param("LD_LIBRARY_PATH"):
    rc_file.write(f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/{mojo_lib_path_from_home}\n")

if param("PATH") is None \
        or "~/.modular/pkg/packages.modular.com_mojo/bin/" not in param("PATH") \
        or f"{home}.modular/pkg/packages.modular.com_mojo/bin/" not in param("PATH"):
    rc_file.write("export PATH=$PATH:~/.modular/pkg/packages.modular.com_mojo/bin/\n")
rc_file.close()

print(f"Please restart your shell or run `source {rc_pth}` to complete the installation")
