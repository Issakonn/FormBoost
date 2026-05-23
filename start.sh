#!/bin/bash
echo "Starting FormBoost..."

uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} &

sleep 1

python3 bot.py &

wait
