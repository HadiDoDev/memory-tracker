#!/bin/bash

crontab memory_tracker/cron/cronjobs
echo user | sudo -S /etc/init.d/cron restart

#uvicorn main:app --host 0.0.0.0 --port 8000 --limit-concurrency 5
gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
