#!/bin/bash

function build_all_tests() {
    files_to_build="ai_test_1.cpp"
    for build_file in $files_to_build; do
        echo "building ${build_file}" 
        vc="g++ -o test ./${build_file}"
        eval "${vc}"
        lt="$?"
        if [[ "${lt}" -ne 0 ]]; then
            echo -e "failed compiling ${build_file} with command:\n${vc}\n"
            exit 1
        else
            echo "compiled ${build_file}"
        fi
    done
}

build_all_tests

exit 0
