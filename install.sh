#!/bin/bash

install() {
  mkdir -p ~/.local/arch-mojo

  cd ~/.local/arch-mojo || return

  curl -sSL https://raw.githubusercontent.com/Sharktheone/arch-mojo/main/install.py -o install.py
  python install.py
}

install