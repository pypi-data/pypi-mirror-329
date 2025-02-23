#! /usr/bin/env bash

function test_blue_flie_README() {
    local options=$1

    abcli_eval ,$options \
        blue_flie build_README
}
