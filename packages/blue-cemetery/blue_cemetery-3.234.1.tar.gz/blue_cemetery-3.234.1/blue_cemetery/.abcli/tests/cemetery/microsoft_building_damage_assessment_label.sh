#! /usr/bin/env bash

function test_blue_sandbox_microsoft_building_damage_assessment_label() {
    local options=$1

    abcli_eval ,$options \
        blue_sandbox_microsoft_building_damage_assessment \
        label \
        ~upload,$options \
        $DAMAGES_TEST_DATASET_OBJECT_NAME \
        "${@:2}"
}
