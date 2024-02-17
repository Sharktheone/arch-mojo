import os
import shutil
import subprocess
import sys
import urllib.request
from getpass import getpass


class Mojo(object):
    __slots__ = ("args", "arch", "home", "working_dir", "mojo_lib_path_from_home", "mojo_lib_path",
                 "install_global", "onlyMojo", "fedora", "skip_next_arg", "authenticated",
                 "rc_pth", "rc_file", "token", "modular"
                 )

    def __init__(self, args: list[str], home: str | None = "~"):
        self.args = args
        self.arch = "x86_64-linux-gnu"
        self.home = home if home is not None else "~"
        self.working_dir = "~/.local/arch-mojo/"
        self.mojo_lib_path_from_home = ".local/lib/mojo"
        self.mojo_lib_path = f"{self.home}/{self.mojo_lib_path_from_home}"
        self.install_global = False
        self.onlyMojo = False
        self.fedora = False
        self.skip_next_arg = False
        self.authenticated = False
        self.rc_pth = None
        self.rc_file = None
        self.token = ""
        self.modular = shutil.which("modular") is not None
        self.is_authenticated()
        self.handle_args()
        self.fedora_os()
        self.install_modular()
        self.ncurses()
        self.install_mojo()
        self.rc_path()
        self.handle_rc()

    def hasstr(self, target: str, original: str) -> bool:
        if not isinstance(target, str) or not isinstance(original, str):
            return False

        elif len(target) > len(original):
            return False
        
        else:
            start = 0
            stop = len(target)

            while start < len(original):
                if original[start:stop] == target:
                    return True
                start += 1
                stop += 1

            else:
                return False

    def _help(self) -> int:
        sys.stdout.write("Usage: python3 install.py [options]")
        sys.stdout.write("Options:")
        sys.stdout.write("  --dir=<path>  | -d=<path>  : Set the working directory")
        sys.stdout.write("  --global      | -g         : Install the libs globally")
        sys.stdout.write("  --help        | -h         : Show this help message")
        sys.stdout.write("  --mojo        | -m         : Only install mojo (modular must be installed)")
        sys.stdout.write("  --fedora      | -f         : Install for fedora")
        sys.stdout.write("  --modular-token <token>    : Set the modular token")
        return 0

    def is_authenticated(self) -> None:
        if self.modular:
            result = subprocess.run(["modular", "config-list"], capture_output=True).stdout.decode("utf-8")
            self.authenticated = self.hasstr("user.id", result)

    def handle_args(self) -> None:
        for arg in self.args:
            if self.skip_next_arg:
                self.skip_next_arg = False
                continue

            if arg.startswith("--dir="):
                self.working_dir = arg.split("=")[1]
            elif arg.startswith("-d="):
                self.working_dir = arg.split("=")[1]
            elif arg == "--global":
                self.install_global = True
            elif arg == "-g":
                self.install_global = True
            elif arg == "--mojo":
                self.onlyMojo = True
            elif arg == "-m":
                self.onlyMojo = True
            elif arg == "--fedora":
                self.fedora = True
            elif arg == "-f":
                self.fedora = True
            elif arg == "--modular-token":
                index = self.args.index(arg) + 1
                
                if index >= len(self.args):
                    sys.stdout.write("\nNo token provided")
                    exit(1)

                if self.token is not None:
                    if self.token == "" or not self.token.startswith("mut_") or not len(self.token) == 36:
                        sys.stdout.write("\nInvalid token")
                        exit(1)

                self.token = self.args[index]
                self.skip_next_arg = True
            
            elif arg == "--help" or arg == "-h":
                exit(self._help())

        self.working_dir = self.working_dir.replace("~", self.home)
        if not self.working_dir.endswith("/"):
            self.working_dir += "/"

        if self.onlyMojo and not self.modular:
            sys.stdout.write("\nModular must be installed to install mojo")
            exit(1)

        try:
            os.makedirs(self.working_dir)
        except OSError:
            pass

    def fedora_os(self) -> None:
        url = "https://ftp.debian.org/debian/pool/main/n/ncurses/libtinfo6_6.4-4_amd64.deb"
        if self.fedora:
            subprocess.run("sudo dnf install binutils", shell=True)

            urllib.request.urlretrieve(url, f"{self.working_dir}libtinfo.deb")
            subprocess.run(f"cd {self.working_dir} && ar -vx libtinfo.deb && tar -xf data.tar.xz", shell=True)
            
            if self.install_global:
                subprocess.run(f"sudo cp {self.working_dir}lib/{self.arch}/libtinfo.so.6.4 /usr/lib/", shell=True)
                subprocess.run("sudo ln -s /usr/lib/libtinfo.so.6.4 /usr/lib/libtinfo.so.6", shell=True)
            else:
                subprocess.run(f"mkdir -p {self.mojo_lib_path}", shell=True)
                subprocess.run(f"cp {self.working_dir}lib/{self.arch}/libtinfo.so.6.4 {self.mojo_lib_path}/libtinfo.so.6", shell=True)

    def install_modular(self) -> None:
        url = "https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/PKGBUILD"
        # install modular if not installed
        if not self.modular:
            # download PKGBUILD
            urllib.request.urlretrieve(url, f"{self.working_dir}PKGBUILD")
            subprocess.run(f"cd {self.working_dir} && makepkg -si", shell=True)

        # authenticate in modular
        if not self.authenticated:
            if self.token is None:
                self.token = os.getenv("MODULAR_TOKEN")
            if self.token is None:
                self.token = getpass("Please enter your Modular auth token: ")
            subprocess.run(f"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{self.mojo_lib_path} modular auth {self.token}", shell=True)

    def ncurses(self) -> None:
        url1 = "https://ftp.debian.org/debian/pool/main/n/ncurses/libncurses6_6.4-4_amd64.deb"
        url2 = "https://ftp.debian.org/debian/pool/main/libe/libedit/libedit2_3.1-20221030-2_amd64.deb"

        # download ncurses lib
        urllib.request.urlretrieve(url1, f"{self.working_dir}libncurses.deb")
        urllib.request.urlretrieve(url2,f"{self.working_dir}libedit.deb")

        os.chdir(f"{self.working_dir}")
        subprocess.run(f"cd {self.working_dir} && ar -vx libncurses.deb && tar -xf data.tar.xz", shell=True)
        subprocess.run(f"cd {self.working_dir} && ar -vx libedit.deb && tar -xf data.tar.xz", shell=True)

        # copy libs
        if self.install_global:
            shutil.copy(f"{self.working_dir}lib/{self.arch}/libncurses.so.6.4", "/lib/libncurses.so.6.4")
            shutil.copy(f"sudo cp {self.working_dir}usr/lib/{self.arch}/libform.so.6.4", "/usr/lib/libform.so.6.4")
            shutil.copy(f"sudo cp {self.working_dir}usr/lib/{self.arch}/libpanel.so.6.4", "/usr/lib/libpanel.so.6.4")
            shutil.copy(f"sudo cp {self.working_dir}usr/lib/{self.arch}/libedit.so.2.0.70", "/usr/lib/libedit.so.2.0.70")

            os.symlink("/lib/libncurses.so.6.4", "/lib/libncurses.so.6")
            os.symlink("/usr/lib/libform.so.6.4", "/usr/lib/libform.so.6")
            os.symlink("/usr/lib/libpanel.so.6.4", "/usr/lib/libpanel.so.6")
            os.symlink("/usr/lib/libedit.so.2.0.70", "/usr/lib/libedit.so.2")
        else:
            try:
                os.mkdir(f"{self.mojo_lib_path}")
            except FileExistsError:
                pass

            shutil.copy(f"{self.working_dir}lib/{self.arch}/libncurses.so.6.4", f"{self.mojo_lib_path}/libncurses.so.6")
            shutil.copy(f"{self.working_dir}usr/lib/{self.arch}/libform.so.6.4", f"{self.mojo_lib_path}/libform.so.6")
            shutil.copy(f"{self.working_dir}usr/lib/{self.arch}/libpanel.so.6.4", f"{self.mojo_lib_path}/libpanel.so.6")
            shutil.copy(f"{self.working_dir}usr/lib/{self.arch}/libedit.so.2.0.70", f"{self.mojo_lib_path}/libedit.so.2")

    def install_mojo(self) -> None:
        # install mojo
        mojo = shutil.which(f"PATH=$PATH:{self.home}/.modular/pkg/packages.modular.com_mojo/bin/ mojo") is not None
        if mojo:
            sys.stdout.write("Mojo is already installed... cleaning up")
            subprocess.run(f"PATH=$PATH:{self.home}/.modular/pkg/packages.modular.com_mojo/bin/ modular clean", shell=True)

        subprocess.run(f"LD_LIBRARY_PATH=$LD_LIBRARY_PATH:{self.mojo_lib_path} modular install mojo", shell=True)

        # fix crashdb directory not found:
        os.makedirs(f"{self.home}/.modular/crashdb", exist_ok=True)

    def get_shell_path(self) -> str | None:
        path = input(
            "\nPlease enter the path to your shell rc file (e.g. ~/.bashrc for bash) or press ENTER to skip:")
        if path == "":
            return None
        return path.replace("~", self.home)

    def get_shell(self, found=None, file=None):
        if found is not None:
            yn = input(f"\nFound {found} shell, add exports to {file}? [y/N/other]: ")
            yn = yn.lower()
            if yn == "y":
                return file
            elif yn == "n":
                return None
            elif yn == "other" or yn == "o":
                return self.get_shell()
            elif yn == "":
                sys.stdout.write("\nSkipping...")
                return None
            else:
                sys.stdout.write("\nInvalid input")
                return self.get_shell(found, file)
        else:
            return self.get_shell_path()

    def rc_path(self) -> str | None:
        shell = os.getenv("SHELL")
        if shell is not None:
            match shell.split("/")[-1]:
                case "bash":
                    return self.get_shell("bash", f"{self.home}/.bashrc")
                case "zsh":
                    return self.get_shell("zsh", f"{self.home}/.zshrc")
                case _:
                    path = input(
                        "\nPlease enter the path to your shell rc file (e.g. ~/.bashrc for bash) or press ENTER to skip:")
                    if path == "":
                        return None
                    return path.replace("~", self.home)

        else:
            return self.get_shell()

    def print_manual_instructions(self) -> None:
        sys.stdout.write("\nPlease add the following to your shell rc file:")
        sys.stdout.write(f"\nexport LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/{self.mojo_lib_path_from_home}")
        sys.stdout.write("\nexport PATH=$PATH:~/.modular/pkg/packages.modular.com_mojo/bin/")

    def handle_rc(self) -> None:
        self.rc_pth = self.rc_path()

        if self.rc_pth is None:
            sys.stdout.write("\nSkipping rc file installation")
            self.print_manual_instructions()
            exit(0)

        else:
            with open(self.rc_pth, "a") as self.rc_file:
                if self.rc_file is None:
                    sys.stdout.write(f"C\nould not open {self.rc_pth}, skipping...")
                    self.print_manual_instructions()
                    exit(0)

                # check if exports are already in rc file
                ld_path = os.getenv("LD_LIBRARY_PATH")
                path = os.getenv("PATH")

                if ld_path is None or not self.hasstr(f"~/{self.mojo_lib_path_from_home}", ld_path) and not self.hasstr(self.mojo_lib_path, ld_path):
                    sys.stdout.write("wrote lib path")
                    self.rc_file.write(f"export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/{self.mojo_lib_path_from_home}\n")

                if path is None or not self.hasstr("~/.modular/pkg/packages.modular.com_mojo/bin/", path) and not self.hasstr(f"{self.home}.modular/pkg/packages.modular.com_mojo/bin/", path):
                    sys.stdout.write("wrote path")
                    self.rc_file.write("export PATH=$PATH:~/.modular/pkg/packages.modular.com_mojo/bin/\n")

            sys.stdout.write(f"\nPlease restart your shell or run `source {self.rc_pth}` to complete the installation\n")


if __name__ == "__main__":
    Mojo(args=sys.argv, home=os.getenv("HOME"))
    sys.exit(0)
