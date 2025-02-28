#!/usr/bin/env bash

set -o errexit

pipenv install --categories "packages unix"

python3 manage.py collectstatic --no-input

python3 manage.py migrate
