#! /usr/bin/env bash

function test_blue_sandbox_cemetery_sagesemseg_train() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)

    abcli_log_warning "🚧 may incur cost 💰, disabled."
    do_dryrun=1

    local dataset_object_name=dataset-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        roofai_dataset_ingest \
        source=AIRS,target=sagemaker,$2 \
        $dataset_object_name \
        --test_count 0 \
        --train_count 16 \
        --val_count 16

    local model_object_name=model-$(abcli_string_timestamp)

    abcli_eval dryrun=$do_dryrun \
        blue_sandbox_cemetery_sagesemseg_train \
        ,$3 \
        $dataset_object_name \
        $model_object_name \
        --instance_type ml.g4dn.2xlarge \
        "${@:4}"
}
