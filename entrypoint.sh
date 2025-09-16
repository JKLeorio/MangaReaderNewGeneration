#! /usr/bin/env bash

set -e


echo "Creating tables..." 
uv run alembic upgrade head

echo "running the app"
uv run main.py