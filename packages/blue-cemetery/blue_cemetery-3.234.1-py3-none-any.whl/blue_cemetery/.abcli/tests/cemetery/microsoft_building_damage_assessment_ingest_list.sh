#! /usr/bin/env bash

function test_blue_sandbox_microsoft_building_damage_assessment_ingest_list() {
    local options=$1

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment_ingest list
    [[ $? -ne 0 ]] && return 1

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment_ingest list \
        event=Maui-Hawaii-fires-Aug-23
    [[ $? -ne 0 ]] && return 1

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment_ingest list \
        event=Maui-Hawaii-fires-Aug-23 \
        04/
}
