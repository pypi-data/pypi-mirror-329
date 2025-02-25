#! /usr/bin/env bash

function test_blue_rover_help() {
    local options=$1

    local module
    for module in \
        "@rover" \
        \
        "@rover pypi" \
        "@rover pypi browse" \
        "@rover pypi build" \
        "@rover pypi install" \
        \
        "@rover pytest" \
        \
        "@rover test" \
        "@rover test list" \
        \
        "blue_rover"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
