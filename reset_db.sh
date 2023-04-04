#!/bin/bash
# this script is used to reset the database for testing purposes only
export FLASK_APP=core/server.py
rm core/store.sqlite3
flask db upgrade -d core/migrations/