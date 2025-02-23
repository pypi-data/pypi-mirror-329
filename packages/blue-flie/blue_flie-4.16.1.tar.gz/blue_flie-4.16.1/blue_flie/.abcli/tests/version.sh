#! /usr/bin/env bash

function test_blue_flie_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_flie version ${@:2}"
}
