#! /usr/bin/env bash

function test_blue_flie_help() {
    local options=$1

    local module
    for module in \
        "@flie" \
        \
        "@flie pypi" \
        "@flie pypi browse" \
        "@flie pypi build" \
        "@flie pypi install" \
        \
        "@flie pytest" \
        \
        "@flie test" \
        "@flie test list" \
        \
        "toolbelt" \
        "toolbelt install" \
        \
        "blue_flie"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
