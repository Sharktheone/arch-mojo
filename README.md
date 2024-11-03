# This is a script to install the mojo programming language on Archlinux and Fedora.

Since mojo needs a version of ncurses that is not available on normal way on Arch, you need to do some extra steps to
get mojo working.

## Arch Installation

You can install mojo either with an AUR helper like `yay` or `paru` by installing the `mojo` package or doing it manually with the following command.

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_libs.py)
```

<details>
<summary>

### Options:

</summary>
Install mojo globally:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_token.py) --global
```

Change working directory:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_libs.py) --dir=/tmp/arch-mojo
```

</details>

## Fedora Installation

First install modular with the official instructions [Modular](https://developer.modular.com/download)

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_libs.py) --fedora
```

<details>
<summary>

### Options:

</summary>
Install mojo globally:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_token.py) --global --fedora
```

Change working directory:

```bash
python <(curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/src/install_libs.py) --dir=/tmp/arch-mojo --fedora
```

</details>


### Missing shared libs

You might get an error about a missing shared library `libpanel.so.6` when mojo is self testing.
That's because modular and python ignores the `LD_LIBRARY_PATH` environment variable.
If you use `mojo` itself it should be set (after you restarted your terminal).
If not add it to your `.bashrc` or `.zshrc`:

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/.local/lib/arch-mojo
```
