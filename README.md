# This is a script to install the mojo programming language on Archlinux.
Since mojo needs a version of ncurses that is not available on normal way on Arch, you need to do some extra steps to get mojo working.

## Installation

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.py)
```
### Options:


Install mojo globally:
```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.sh) --global
```

Change working directory:
```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.sh) --dir=/tmp/arch-mojo
```
