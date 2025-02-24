#!/bin/bash
set -e
PROJECT_ROOT="$(dirname "$0")/.."

cd "$PROJECT_ROOT"
if [[ $(uname) == "Linux" ]]; then
        pylint .\
        --fail-under=9.0 \
        --fail-on=W,E \
        lib \
        widgets \
        $@
    elif [[ $(uname) == "CYGWIN"* || $(uname) == "MINGW"* ]]; then
        python -m pylint \
        --fail-under=9.0 \
        --fail-on=W,E \
        lib \
        widgets \
        $@
    fi
