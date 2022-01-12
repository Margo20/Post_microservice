#!/bin/bash

worker_ready() {
    celery -A celery_worker.celery_app inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers is available'

celery flower \
    --app=celery_worker.celery_app \
    --broker="${CELERY_BROKER_URL}"
