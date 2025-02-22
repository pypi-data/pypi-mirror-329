#! /usr/bin/env bash

function test_roofai_help() {
    local options=$1

    local module
    for module in \
        "@gearth" \
        "@google_earth" \
        "@google_earth browse" \
        "@google_earth fetch" \
        \
        "@gmaps" \
        "@google_maps" \
        "@google_maps get_static_image" \
        "@google_maps geocode" \
        "@google_maps predict" \
        \
        "@roboflow" \
        "@roboflow create_project" \
        "@roboflow download" \
        "@roboflow status" \
        "@roboflow upload" \
        \
        "roofai dataset" \
        "roofai dataset ingest" \
        "roofai dataset review" \
        \
        "roofai semseg" \
        "roofai semseg predict" \
        "roofai semseg train" \
        \
        "roofai"; do
        abcli_eval ,$options \
            abcli_help $module
        [[ $? -ne 0 ]] && return 1

        abcli_hr
    done

    return 0
}
