import os
import shutil
import subprocess
import urllib.request

# TODO use shutil to copy files

arch = "x86_64-linux-gnu"

answers = {}


answers["venv"] = input(
    "Do you want to automatically use a venv when running modular install/update? (y/n): ").lower() == "y"


modular = shutil.which("modular") is not None
venv = os.environ["MOJO_VENV"] is not None
authenticated = subprocess.run(["modular", "config-list"], capture_output=True).stdout.decode("utf-8") == "true"

token = input("Please enter your Modular auth token. You can also type 'manual' to run "
              "modular manually when requested: ")


def param(name: str):
    try:
        return os.environ[name]
    except:
        return None


install_global = param("ARCH_MOJO_GLOBAL") is not None

WORKING_DIR = param("ARCH_MOJO_WORKING_DIR") if param("ARCH_MOJO_WORKING_DIR") is not None else "~/.local/arch-mojo/"

WORKING_DIR = WORKING_DIR.replace("~", os.environ["HOME"])

if WORKING_DIR[-1] != "/":
    WORKING_DIR += "/"

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

os.system(f"modular auth {token}")


# download ncurses lib

urllib.request.urlretrieve("http://ftp.debian.org/debian/pool/main/n/ncurses/libncurses6_6.4-4_amd64.deb",
                           f"{WORKING_DIR}libncurses.deb")

urllib.request.urlretrieve("http://ftp.debian.org/debian/pool/main/libe/libedit/libedit2_3.1-20221030-2_amd64.deb",
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

os.system(f"python3 -m venv {WORKING_DIR}venv")
os.system(f"source {WORKING_DIR}venv/bin/activate && modular install mojo")


def rc_path():
    match os.environ["SHELL"].split("/")[-1]:
        case "bash":
            return f"{os.environ['HOME']}/.bashrc"
        case "zsh":
            return f"{os.environ['HOME']}/.zshrc"
        case _:
            path = input("Please enter the path to your shell rc file (e.g. ~/.bashrc for bash): ")
            return path.replace("~", os.environ["HOME"])


rc_file = open(rc_path(), "a")
shell_rc = open(rc_path(), "r").read()

if (venv
        and "function modular()" not in shell_rc
        and "function mojo()" not in shell_rc):
    os.system(f"python3 -m venv {WORKING_DIR}venv")
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/shell.sh",
                               f"{WORKING_DIR}shell.sh")
    shell_file = open(f"{WORKING_DIR}shell.sh", "r")
    shell = shell_file.read()

    shell = shell.replace("{{venv-path}}", f"{WORKING_DIR}venv")

    rc_file.write(shell)

exports = \
    """
    
# added by arch-mojo script
export PATH=$PATH:~/.modular/pkg/packages.modular.com_mojo/bin/
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib/mojo
"""

home = os.environ["HOME"]

# check if exports are already in rc file
try:
    if (("~/.modular/pkg/packages.modular.com_mojo/bin/" not in os.environ["PATH"]
         or f"{home}/.modular/pkg/packages.modular.com_mojo/bin/" not in os.environ["LD_LIBRARY_PATH"])
            and
            ("~/.local/lib/mojo" not in os.environ["LD_LIBRARY_PATH"]
             or f"{home}/.local/lib/mojo" not in os.environ["LD_LIBRARY_PATH"])):
        rc_file.write(exports)
except:
    rc_file.write(exports)

rc_file.close()

# # delete temp files
# # maybe here a check would make sense if the WORKING_DIR is already existing
#
# if WORKING_DIR.split("/")[1] == "tmp":
#     exit(0)
#
#
# #TODO list all created files and don't do this manually
#
# created_files = [
#     "PKGBUILD",
#     "libncurses.deb",
#     "data.tar.xz",
#     "control.tar.xz",
#     "shell.sh",
#     "venv",
#     f"lib/{arch}/*",
#     f"usr/lib/{arch}/*",
#     "usr/share/doc/*",
#     "modular-0.1.4-1-x86_64.pkg.tar.zst",
#     "modular-0.1.4-amd64.deb",
#     "debian-binary",
#     "pkg/modular/etc/modular/*",
#     "pkg/modular/usr/bin/*",
#     "pkg/modular/usr/share/man/man1/*",
#     "src/*"
#
# ]
#
# if not answers["venv"]:
#     os.system(f"rm -r {WORKING_DIR}venv")
#
# for file in created_files:
#     os.system(f"rm {WORKING_DIR}{file}")
