#!/usr/bin/env bash

basedir="$(cd "$(dirname "${BASH_SOURCE}")" >/dev/null; pwd)" || exit 1

cd "${basedir}"
ansible-playbook main.yaml --ask-become-pass "$@"
