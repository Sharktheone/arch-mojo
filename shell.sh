function modular() {
    if [[ "$1" == "install" ]] ||  [[ "$1" == "uninstall" ]]; then
        source {{venv-path}}/bin/activate
    fi
    command modular "$@"
}

function mojo() {
    if [[ "$1" == "update" ]]; then
        source {{venv-path}}/bin/activate
        modular uninstall mojo
        modular clean
        modular install mojo
    else
        command mojo "$@"
    fi
}
