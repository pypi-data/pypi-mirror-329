#!/bin/bash

update_software() {
    pip install price_updater --upgrade
}

start_program() {
    python -m price_updater
}

update_software
start_program