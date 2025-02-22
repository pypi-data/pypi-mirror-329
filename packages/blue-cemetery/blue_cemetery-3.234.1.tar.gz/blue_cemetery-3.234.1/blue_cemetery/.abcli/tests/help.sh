#! /usr/bin/env bash

function test_blue_cemetery_help() {
    local options=$1

    local module
    for module in \
        "@cemetery" \
        \
        "@cemetery pypi" \
        "@cemetery pypi browse" \
        "@cemetery pypi build" \
        "@cemetery pypi install" \
        \
        "@cemetery pytest" \
        \
        "@cemetery test" \
        "@cemetery test list" \
        \
        "blue_cemetery"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
