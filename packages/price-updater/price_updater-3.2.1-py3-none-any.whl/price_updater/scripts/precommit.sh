#!/bin/bash
PROJECT_ROOT="$(dirname "$0")/.."
set -e
cd "$PROJECT_ROOT/scripts"
./black.sh
./mypy.sh
./pylint.sh
