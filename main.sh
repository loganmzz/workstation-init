#!/usr/bin/env bash

basedir="$(cd "$(dirname "${BASH_SOURCE}")" >/dev/null; pwd)" || exit 1

cd "${basedir}"
args=(--ask-become-pass)
[[ $# == 0 ]] || {
    args+=(--extra-vars "$(jq '{enabled_tasks:$ARGS.positional}' --args "$@" -c -n)")
}
ansible-playbook main.yaml "${args[@]}"
