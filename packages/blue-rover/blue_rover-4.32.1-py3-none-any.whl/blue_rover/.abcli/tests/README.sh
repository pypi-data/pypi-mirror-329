#! /usr/bin/env bash

function test_blue_rover_README() {
    local options=$1

    abcli_eval ,$options \
        blue_rover build_README
}



