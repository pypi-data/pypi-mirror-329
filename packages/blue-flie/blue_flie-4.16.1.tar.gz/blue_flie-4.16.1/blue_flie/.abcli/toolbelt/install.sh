#! /usr/bin/env bash

function blue_flie_toolbelt_install() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_eval dryrun=$do_dryrun \
        docker run --rm -it bitcraze/toolbelt
}

function abcli_install_blue_flie_toolbelt() {
    abcli_git_clone https://github.com/bitcraze/toolbelt.git
}

abcli_install_module blue_flie_toolbelt 1.1.1
