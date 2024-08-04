import os.path
import shutil
import subprocess
import sys
import urllib.request

INSTALL_DIR = "~/.local/lib/arch-mojo"
ARCH = "x86_64-linux-gnu"

TEMP_DIR = "/tmp/mojo_libs"


def print_help():
    print("Usage: python3 install_libs.py [options]")
    print("Options:")
    print("  --dir <path>  | -d <path>  : Install directory")
    print("  --arch <arch> | -a <arch>  : Architecture")
    print("  --help        | -h         : Display this help message")
    print("  --fedora      | -f         : Install Fedora libraries")
    exit(0)


class MojoLibs:
    def __init__(self):
        self.install_dir = INSTALL_DIR
        self.arch = ARCH
        self.handle_args()

        self.install_libs()
        self.print_failture_information()

        #TODO: Add lib folder to LD_LIBRARY_PATH

    def handle_args(self):
        skip_next = False

        def assert_next_arg(idx):
            if idx + 1 >= len(sys.argv[1:]):
                print("Error: Missing argument for " + sys.argv[idx])
                exit(1)

        for i, arg in enumerate(sys.argv[1:]):
            if skip_next:
                skip_next = False
                continue

            if arg == "--dir" or arg == "-d":
                assert_next_arg(i)

                self.install_dir = sys.argv[i + 1]
                skip_next = True

            elif arg == "--arch" or arg == "-a":
                assert_next_arg(i)

                self.arch = sys.argv[i + 1]
                skip_next = True

            elif arg == "--help" or arg == "-h":
                print_help()
            elif arg == "--fedora" or arg == "-f":
                self.install_fedora()
                exit(0)
            else:
                print_help()

    def install_fedora(self):
        sys.stderr.write("Error: Fedora installation not supported yet\n")  # TODO
        exit(1)

    def install_libs(self):
        print(f"Installing libraries to `{self.install_dir}` for `{self.arch}`")

        libncruses = "https://ftp.debian.org/debian/pool/main/n/ncurses/libncurses6_6.4-4_amd64.deb"
        libedit = "https://ftp.debian.org/debian/pool/main/libe/libedit/libedit2_3.1-20221030-2_amd64.deb"

        # download deb libraries

        urllib.request.urlretrieve(libncruses, os.path.join(TEMP_DIR, "libncurses.deb"))
        urllib.request.urlretrieve(libedit, os.path.join(TEMP_DIR, "libedit.deb"))

        subprocess.run(f"cd {TEMP_DIR} && ar -vx libncurses.deb && tar -xf data.tar.xz", shell=True, check=True)
        subprocess.run(f"cd {TEMP_DIR} && ar -vx libedit.deb && tar -xf data.tar.xz", shell=True, check=True)

        try:
            os.makedirs(self.install_dir)
        except FileExistsError:
            pass

        # move the needed libraries

        shutil.copy(f"{TEMP_DIR}/lib/{self.arch}/libncurses.so.6.4", os.path.join(self.install_dir, "libncurses.so.6"))
        shutil.copy(f"{TEMP_DIR}/usr/lib/{self.arch}/libform.so.6.4", os.path.join(self.install_dir, "libform.so.6"))
        shutil.copy(f"{TEMP_DIR}/usr/lib/{self.arch}/libpanel.so.6.4", os.path.join(self.install_dir, "libpanel.so.6"))
        shutil.copy(f"{TEMP_DIR}/usr/lib/{self.arch}/libedit.so.2.0.70", os.path.join(self.install_dir, "libedit.so.2"))

    def print_failture_information(self) -> None:
        sys.stdout.write(
            "\n\033[41;37mTL;DR: If you see errors, ignore them or report them to https://https://github.com/Sharktheone/arch-mojo and restart your shell\033[0m\n")
        sys.stdout.write(
            "\n\033[91mPlease note that you might be seeing some errors about some components that weren't installed correctly\033[0m\n")
        sys.stdout.write(
            "\n\033[91mFor more information see here: https://github.com/Sharktheone/arch-mojo?tab=readme-ov-file#missing-shared-libs\033[0m\n")
        sys.stdout.write(
            "\n\033[91mPlease do not report any installation errors to Modular, as this is not an official installation method\033[0m\n")
        sys.stdout.write(
            "\n\033[91mIf you encounter any issues, please report them to https://github.com/Sharktheone/arch-mojo/issues\033[0m\n")
        sys.stdout.write("It would also be nice if you starred the repo, thanks! ❤️\n")
