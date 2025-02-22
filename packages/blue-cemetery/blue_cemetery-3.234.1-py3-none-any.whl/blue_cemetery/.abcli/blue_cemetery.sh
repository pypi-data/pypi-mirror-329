#! /usr/bin/env bash

function blue_cemetery() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=blue_cemetery,task=$task \
        "${@:2}"
}

abcli_log $(blue_cemetery version --show_icon 1)
