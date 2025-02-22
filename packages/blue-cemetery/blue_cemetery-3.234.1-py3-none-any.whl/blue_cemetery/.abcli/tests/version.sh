#! /usr/bin/env bash

function test_blue_cemetery_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_cemetery version ${@:2}"
}



