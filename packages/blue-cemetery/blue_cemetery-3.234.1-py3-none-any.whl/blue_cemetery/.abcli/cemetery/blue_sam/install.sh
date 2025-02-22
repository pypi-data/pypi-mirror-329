#! /usr/bin/env bash

function blue_sandbox_blue_sam_install() {
    local env_name=blue_sam

    if [[ $(abcli_conda_exists name=$env_name) == 1 ]]; then
        abcli_conda_rm name=$env_name
        [[ $? -ne 0 ]] && return 1
    fi

    conda create -n $env_name python
    [[ $? -ne 0 ]] && return 1

    conda activate $env_name
    [[ $? -ne 0 ]] && return 1

    conda install -c conda-forge mamba
    [[ $? -ne 0 ]] && return 1

    mamba install -c conda-forge segment-geospatial
}
