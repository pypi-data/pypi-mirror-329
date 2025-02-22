#! /usr/bin/env bash

function test_blue_cemetery_README() {
    local options=$1

    abcli_eval ,$options \
        blue_cemetery build_README
}



