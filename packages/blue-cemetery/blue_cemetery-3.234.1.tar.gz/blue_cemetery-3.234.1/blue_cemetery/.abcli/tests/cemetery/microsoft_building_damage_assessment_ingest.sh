#! /usr/bin/env bash

function test_blue_sandbox_microsoft_building_damage_assessment_ingest() {
    local options=$1

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment \
        ingest \
        event=Maui-Hawaii-fires-Aug-23,~upload,$options \
        test_blue_sandbox_microsoft_building_damage_assessment_ingest-$(abcli_string_timestamp_short) \
        --verbose 1 \
        "${@:2}"
}
