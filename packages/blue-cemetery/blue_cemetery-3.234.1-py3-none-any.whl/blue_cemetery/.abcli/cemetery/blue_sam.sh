#! /usr/bin/env bash

function blue_sandbox_blue_sam() {
    local task=$(abcli_unpack_keyword $1 help)

    local function_name=blue_sandbox_blue_sam_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m blue_sandbox.blue_sam "$@"
}

abcli_source_caller_suffix_path /blue_sam
