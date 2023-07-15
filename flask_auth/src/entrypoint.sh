#!/bin/bash
exec python3 -u ./ping.py &
exec alembic upgrade head &
exec python3 -u pywsgi.py