#! /usr/bin/env bash

function blue_sandbox_microsoft_building_damage_assessment_tensorboard() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_browse=$(abcli_option_int "$options" browse $(abcli_not $do_dryrun))
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local port=$(abcli_option "$options" port 8889)

    local model_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $model_object_name

    [[ "$do_browse" == 1 ]] &&
        abcli_browse http://localhost:$port/

    abcli_eval ,$options \
        tensorboard \
        --logdir $ABCLI_OBJECT_ROOT/$model_object_name/logs/ \
        --port $port
}
