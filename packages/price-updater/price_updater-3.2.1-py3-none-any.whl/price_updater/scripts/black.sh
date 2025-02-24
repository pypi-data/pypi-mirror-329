#!/bin/bash
set -e
PROJECT_ROOT="$(dirname "$0")/.."

cd "$PROJECT_ROOT"

if [ $# -ge 1 ]; then
    if [ "$1" != "--check" ]; then
        echo "Invalid arguments"
        exit 1
    fi
    FLAGS="--check"
else
    FLAGS="./"
    if [[ $(uname) == "Linux" ]]; then
        black . $FLAGS
    elif [[ $(uname) == "CYGWIN"* || $(uname) == "MINGW"* ]]; then
        python -m black $FLAGS
    fi
fi