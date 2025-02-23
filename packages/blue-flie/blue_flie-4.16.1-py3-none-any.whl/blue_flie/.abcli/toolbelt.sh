#! /usr/bin/env bash

function blue_flie_toolbelt() {
    local task=$(abcli_unpack_keyword $1 void)

    local function_name=blue_flie_toolbelt_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    abcli_log_error "toolbelt: task not found."
}

abcli_source_caller_suffix_path /toolbelt
