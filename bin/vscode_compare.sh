#!/usr/bin/env bash

basedir="$(cd "$(dirname "${BASH_SOURCE}")/.." >/dev/null; pwd)" || exit 1

SRC_PATH=~/.config/Code/User
TGT_PATH="${basedir}/files/vscode/config"

cd "${TGT_PATH}"
for file in $(find . -type f); do
    existing_backups="$(\ls -x "${SRC_PATH}/${file}".* 2>/dev/null | xargs --no-run-if-empty -- realpath)"
    [[ -z "${existing_backups}" ]] || {
        echo "------------------------------------------------"
        echo "Found backups:"
        echo "${existing_backups}"
    }
    code --diff "${SRC_PATH}/${file}" "${TGT_PATH}/${file}"
done

cd "${SRC_PATH}/snippets"
for file in $(find . -name '*.json'); do
    [[ -f "${TGT_PATH}/snippets/${file}" ]] || {
        echo "No sources for '$(realpath "${SRC_PATH}/snippets/${file}")'"
    }
done
