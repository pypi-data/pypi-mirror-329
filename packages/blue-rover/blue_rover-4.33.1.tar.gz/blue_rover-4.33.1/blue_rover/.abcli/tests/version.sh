#! /usr/bin/env bash

function test_blue_rover_version() {
    local options=$1

    abcli_eval ,$options \
        "blue_rover version ${@:2}"
}



