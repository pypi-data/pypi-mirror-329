#! /usr/bin/env bash

function blue_cemetery_browse() {
    local options=$1
    local what=$(abcli_option_choice "$options" actions,repo repo)

    local url="https://github.com/kamangir/blue-cemetery"
    [[ "$what" == "actions" ]] &&
        url="$url/actions"

    abcli_browse $url
}
