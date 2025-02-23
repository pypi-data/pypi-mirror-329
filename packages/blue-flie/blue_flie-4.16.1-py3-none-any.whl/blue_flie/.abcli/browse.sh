#! /usr/bin/env bash

function blue_flie_browse() {
    local options=$1
    local what=$(abcli_option_choice "$options" actions,repo repo)

    local url="https://github.com/kamangir/blue-flie"
    [[ "$what" == "actions" ]] &&
        url="$url/actions"

    abcli_browse $url
}
