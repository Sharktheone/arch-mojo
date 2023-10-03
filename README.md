# This is a script to install the mojo programming language on Archlinux.
Since mojo needs a version of ncurses that is not available on normal way on Arch, you need to do some extra steps to get mojo working.

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.sh | bash
```
### Options:


Install mojo globally:
```bash
ARCH_MOJO_GLOBAL=true curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.sh | bash
```

Change working directory:
```bash
ARCH_MOJO_WORKDIR=/tmp/arch-mojo curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.sh | bash
```
