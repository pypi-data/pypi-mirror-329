#! /usr/bin/env bash

function blue_flie() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=blue_flie,task=$task \
        "${@:2}"
}

abcli_log $(blue_flie version --show_icon 1)
