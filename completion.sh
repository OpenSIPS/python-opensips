function _opensips-mi-complete() {
    local cur prev opts completed_args
    COMPREPLY=()

    cur="${COMP_WORDS[COMP_CWORD]}"

    prev="${COMP_WORDS[COMP_CWORD-1]}"

    completed_args=""
    if [[ "${prev:0:1}" != "-" ]]; then
        if [[ $COMP_CWORD -ge 2 ]]; then
            completed_args="${COMP_WORDS[@]:1:COMP_CWORD-2}"
            if [[ "${COMP_WORDS[COMP_CWORD-2]:0:1}" == "-" ]]; then
                completed_args="$completed_args $prev"
            fi
        fi
        opts="$(opensips-mi $completed_args -bc)"
    else
        while [[ "${prev:0:1}" == "-" ]]; do
            prev="${prev:1}"
        done
        completed_args="${COMP_WORDS[@]:1:COMP_CWORD-2}"
        opts="$(opensips-mi -bc $prev)"
    fi

    COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}

complete -F _opensips-mi-complete opensips-mi

function _opensips-event-complete() {
    local cur prev opts completed_args
    COMPREPLY=()

    cur="${COMP_WORDS[COMP_CWORD]}"

    prev="${COMP_WORDS[COMP_CWORD-1]}"

    completed_args=""
    if [[ "${prev:0:1}" != "-" ]]; then
        if [[ $COMP_CWORD -ge 2 ]]; then
            completed_args="${COMP_WORDS[@]:1:COMP_CWORD-2}"
            if [[ "${COMP_WORDS[COMP_CWORD-2]:0:1}" == "-" ]]; then
                completed_args="$completed_args $prev"
            fi
        fi
        opts="$(opensips-event $completed_args -bc)"
    else
        while [[ "${prev:0:1}" == "-" ]]; do
            prev="${prev:1}"
        done
        completed_args="${COMP_WORDS[@]:1:COMP_CWORD-2}"
        opts="$(opensips-event -bc $prev)"
    fi

    COMPREPLY=( $(compgen -W "$opts" -- "$cur") )
}

complete -F _opensips-event-complete opensips-event