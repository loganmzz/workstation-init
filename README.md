Default Workstation setup
===

# Purpose

This repository aims to setup a workstation for development based on some prerequesites.

# Prequesites

## Ubuntu 22.04

## pip

```bash
wget https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```

## Ansible 6.3.0

```bash
python3 -m pip install --user ansible==6.3.0
```

## Git

```bash
sudo add-apt-repository ppa:git-core/ppa
sudo apt update
sudo apt install git
```

# Usage

```bash
~/.local/bin/ansible-playbook --ask-become-pass main.yaml
```
