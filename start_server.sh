#!/usr/bin/env bash
export PYTHONPATH=$PWD
pipenv run gunicorn -b 127.0.0.1:8001 --log-level=DEBUG --workers=2 --timeout=90 'pmapi.app:app'
