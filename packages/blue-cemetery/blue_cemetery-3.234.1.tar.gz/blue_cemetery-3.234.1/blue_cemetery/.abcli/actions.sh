#! /usr/bin/env bash

function blue_cemetery_action_git_before_push() {
    blue_cemetery build_README
    [[ $? -ne 0 ]] && return 1

    [[ "$(abcli_git get_branch)" != "main" ]] &&
        return 0

    blue_cemetery pypi build
}
