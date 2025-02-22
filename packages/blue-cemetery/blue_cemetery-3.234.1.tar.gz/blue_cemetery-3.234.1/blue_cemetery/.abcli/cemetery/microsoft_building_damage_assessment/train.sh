#! /usr/bin/env bash

function blue_sandbox_microsoft_building_damage_assessment_train() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local do_download=$(abcli_option_int "$options" download $(abcli_not $do_dryrun))
    local do_upload=$(abcli_option_int "$options" upload $(abcli_not $do_dryrun))

    local dataset_object_name=$(abcli_clarify_object $2 .)
    [[ "$do_download" == 1 ]] &&
        abcli_download - $dataset_object_name

    local model_object_name=$(abcli_clarify_object $3 $dataset_object_name-model-$(abcli_string_timestamp_short))

    abcli_log "training $dataset_object_name -> $model_object_name ..."

    conda activate bda
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun \
        python3 -m blue_sandbox.microsoft_building_damage_assessment \
        train \
        --dataset_object_name $dataset_object_name \
        --model_object_name $model_object_name \
        "${@:4}"
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun,path=$abcli_path_git/building-damage-assessment \
        python3 project_setup.py \
        --skip_health_check \
        --config $ABCLI_OBJECT_ROOT/$model_object_name/config.yml
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun,path=$abcli_path_git/building-damage-assessment \
        python3 create_masks.py \
        --config $ABCLI_OBJECT_ROOT/$model_object_name/config.yml
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun,path=$abcli_path_git/building-damage-assessment \
        python3 fine_tune.py \
        --config $ABCLI_OBJECT_ROOT/$model_object_name/config.yml
    [[ $? -ne 0 ]] && return 1

    abcli_eval dryrun=$do_dryrun,path=$abcli_path_git/building-damage-assessment \
        python3 inference.py \
        --config $ABCLI_OBJECT_ROOT/$model_object_name/config.yml
    [[ $? -ne 0 ]] && return 1

    [[ "$do_upload" == 1 ]] &&
        abcli_upload - $model_object_name

    return 0
}
