import os

os.system("python3 -m venv /tmp/arch-mojo/venv")
os.system("source /tmp/arch-mojo/venv/bin/activate")
os.system("pip install inquirer")

import inquirer
import urllib.request

arch = "x86_64-linux-gnu"

questions = [
    inquirer.Confirm("modular", message="Do you already have modular installed?"),
    inquirer.Confirm("persistent", message="Do you want to install the libraries persistent?"),
    inquirer.Confirm("venv", message="Do you want to automatically use a venv when running modular install/update?"),
    inquirer.Path("path", message="Where do you want to create the venv and temporary files (the venv is needed for "
                                  "installation anyways)", path_type=inquirer.Path.DIRECTORY),
    inquirer.Password("token", message="Please enter your Modular auth token. You can also type 'manual' to run "
                                       "modular manually when requested"),
]

answers = inquirer.prompt(questions)

WORKING_DIR = answers["path"]
if WORKING_DIR[-1] != "/":
    WORKING_DIR += "/"

# install modular if not installed
if answers["modular"]:
    # download PKGBUILD
    urllib.request.urlretrieve("https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/PKGBUILD",
                               f"{WORKING_DIR}PKGBUILD")
    os.system(f"cd {WORKING_DIR} && makepkg -si")

# authenticate in modular
if answers["token"] != "manual":
    os.system(f"modular auth {answers['token']}")
else:
    print("Please run 'modular auth <token>' to authenticate yourself")
    input("Press enter to continue")

# download ncurses lib

urllib.request.urlretrieve("http://ftp.debian.org/debian/pool/main/n/ncurses/libncurses6_6.4-4_amd64.deb",
                           f"{WORKING_DIR}libncurses.deb")

os.system(f"cd {WORKING_DIR} && ar -vx libncurses.deb && tar -xf data.tar.xz")

# copy libs

if answers["persistent"]:
    os.system(f"sudo cp {WORKING_DIR}lib/{arch}/* /lib/")
    os.system(f"sudo cp {WORKING_DIR}usr/lib/{arch}/* /usr/lib/")
    os.system(f"sudo cp {WORKING_DIR}lib/{arch}/* /usr/lib/")


else:
    mojo_lib_path = "/home/$USER/.modular/pkg/packages.modular.com_mojo/lib"

    os.system(f"mkdir -p {mojo_lib_path}")

    os.system(f"cp {WORKING_DIR}lib/{arch}/libncurses.so.6.4 {mojo_lib_path}/libncurses.so.6")
    os.system(f"cp {WORKING_DIR}lib/{arch}/libform.so.6.4 {mojo_lib_path}/libform.so.6")
    os.system(f"cp {WORKING_DIR}lib/{arch}/libpanel.so.6.4 {mojo_lib_path}/libncurses.so.6.4")

# install mojo

os.system(f"python3 -m venv {WORKING_DIR}venv")
os.system(f"source {WORKING_DIR}venv/bin/activate")
os.system("modular install mojo")
