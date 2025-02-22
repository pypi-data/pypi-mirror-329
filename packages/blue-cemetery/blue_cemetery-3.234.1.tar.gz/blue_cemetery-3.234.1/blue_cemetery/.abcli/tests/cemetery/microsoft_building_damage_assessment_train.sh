#! /usr/bin/env bash

function test_blue_sandbox_microsoft_building_damage_assessment_train() {
    local options=$1

    abcli_log_warning "disabled."
    return 0

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment \
        train \
        ~upload,$options \
        $DAMAGES_TEST_DATASET_OBJECT_NAME \
        test_blue_sandbox_microsoft_building_damage_assessment_train-$(abcli_string_timestamp_short) \
        --verbose 1 \
        "${@:2}"

    # ignore error - TODO: disable
    return 0
}
