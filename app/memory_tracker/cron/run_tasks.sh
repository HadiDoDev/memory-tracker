#!/bin/bash
# shellcheck disable=SC2155

export PRODUCTION_MODE=True
export PYTHONPATH=/srv/memory_tracker/
/usr/local/bin/python /srv/memory_tracker/memory_tracker/cron/tasks.py
