#! /usr/bin/env bash

function blue_rover() {
    local task=$(abcli_unpack_keyword $1 version)

    abcli_generic_task \
        plugin=blue_rover,task=$task \
        "${@:2}"
}

abcli_log $(blue_rover version --show_icon 1)
