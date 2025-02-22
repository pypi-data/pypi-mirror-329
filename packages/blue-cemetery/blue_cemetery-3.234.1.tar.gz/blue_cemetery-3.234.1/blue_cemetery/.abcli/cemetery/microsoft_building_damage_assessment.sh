#! /usr/bin/env bash

function blue_sandbox_microsoft_building_damage_assessment() {
    local task=$(abcli_unpack_keyword $1 help)

    local function_name=blue_sandbox_microsoft_building_damage_assessment_$task
    if [[ $(type -t $function_name) == "function" ]]; then
        $function_name "${@:2}"
        return
    fi

    python3 -m blue_sandbox.microsoft_building_damage_assessment "$@"
}

abcli_source_caller_suffix_path /microsoft_building_damage_assessment
