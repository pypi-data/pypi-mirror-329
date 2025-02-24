#!/bin/bash
set -e
PROJECT_ROOT="$(dirname "$0")/.."

cd "$PROJECT_ROOT"
if [[ $(uname) == "Linux" ]]; then
        mypy . $FLAGS
    elif [[ $(uname) == "CYGWIN"* || $(uname) == "MINGW"* ]]; then
        python -m mypy .
    fi
