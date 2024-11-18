#!/bin/bash

CMD=$1
shift

if [[ $CMD == *.py ]]; then
    TOOL=python3
elif [[ $CMD == *.sh ]]; then
    TOOL=bash
else
    TOOL=opensips-mi
fi

exec $TOOL $CMD "$@"

