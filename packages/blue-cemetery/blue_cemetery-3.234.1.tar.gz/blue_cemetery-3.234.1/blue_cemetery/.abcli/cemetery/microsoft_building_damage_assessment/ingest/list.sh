#! /usr/bin/env bash

function blue_sandbox_microsoft_building_damage_assessment_ingest_list() {
    local options=$1
    local event_name=$(abcli_option "$options" event all)

    local suffix=$2

    local url="s3://maxar-opendata/events/"

    [[ "$event_name" != all ]] &&
        url="$url$event_name/ard/"

    [[ ! -z "$suffix" ]] &&
        url="$url$suffix"

    abcli_eval ,$options \
        aws s3 ls --no-sign-request $url

    return 0
}
