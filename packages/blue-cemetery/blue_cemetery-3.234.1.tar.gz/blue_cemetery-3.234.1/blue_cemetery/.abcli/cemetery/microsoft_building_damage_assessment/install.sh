#! /usr/bin/env bash

function blue_sandbox_microsoft_building_damage_assessment_install() {
    local options=$1
    local do_dryrun=$(abcli_option_int "$options" dryrun 0)
    local recreate_env=$(abcli_option_int "$options" recreate_env 0)

    if [[ -d "$abcli_path_git/building-damage-assessment" ]]; then
        abcli_log "✅  building-damage-assessment"
    else
        abcli_git_clone https://github.com/microsoft/building-damage-assessment.git
        [[ $? -ne 0 ]] && return 1
    fi

    [[ "$abcli_is_github_workflow" == true ]] ||
        [[ "$abcli_is_sagemaker_system" == true ]] &&
        return 0

    if [[ "$recreate_env" == 1 ]]; then
        abcli_conda_rm name=bda
        [[ $? -ne 0 ]] && return 1
    fi

    local exists=$(abcli_conda_exists name=bda)
    if [[ "$exists" == 0 ]]; then
        # https://github.com/microsoft/building-damage-assessment?tab=readme-ov-file#setup
        conda env create \
            -f $abcli_path_git/building-damage-assessment/environment.yml
        [[ $? -ne 0 ]] && return 1
    fi

    conda activate bda
    [[ $? -ne 0 ]] && return 1

    pushd $abcli_path_git/blue-sandbox >/dev/null
    pip3 install -e .
    [[ $? -ne 0 ]] && return 1
    popd >/dev/null

    [[ "$abcli_is_mac" == true ]] &&
        brew install wget

    return 0
}

function abcli_install_microsoft_building_damage_assessment() {
    blue_sandbox_microsoft_building_damage_assessment_install "$@"
}

abcli_install_module microsoft_building_damage_assessment 1.1.1
