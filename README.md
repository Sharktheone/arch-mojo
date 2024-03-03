# This is a script to install the mojo programming language on Archlinux and Fedora.

Since mojo needs a version of ncurses that is not available on normal way on Arch, you need to do some extra steps to
get mojo working.

## Arch Installation

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py)
```

<details>
<summary>

### Options:

</summary>
Install mojo globally:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py) --global
```

Change working directory:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py) --dir=/tmp/arch-mojo
```

</details>

## Fedora Installation

First install modular with the official instructions [Modular](https://developer.modular.com/download)

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py) --fedora
```

<details>
<summary>

### Options:

</summary>
Install mojo globally:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py) --global --fedora
```

Change working directory:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install.py) --dir=/tmp/arch-mojo --fedora
```

</details>
