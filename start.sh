#!/bin/bash
uvicorn server:app --host 0.0.0.0 --port ${PORT:-8000} &
sleep 2
python3 bot.py &
wait
