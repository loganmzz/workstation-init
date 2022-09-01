#!/usr/bin/env bash

basedir="$(cd "$(dirname "${BASH_SOURCE}")/.." >/dev/null; pwd)" || exit 1

SRC_PATH=~/.config/Code/User
TGT_PATH="${basedir}/files/vscode"

cd "${TGT_PATH}"
for file in $(find . -type f); do
    code --diff "${SRC_PATH}/${file}" "${TGT_PATH}/${file}"
done
