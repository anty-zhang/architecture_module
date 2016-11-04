#!/bin/bash

echo `dirname "$0"`
echo "$0"

function usage() {
    echo "Usage: "
    exit 0
}

if [[ "$@" = *--help ]] || [[ "$@" = *-h ]]; then
    usage
fi
