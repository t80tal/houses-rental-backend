#!/bin/sh
# Just execute this file in order to run the server
# By typing the FILEPATH in the terminal, Example: ./run.sh
# To make it executable use: chmod u+x FILEPATH
. ./venv/bin/activate
cd backend
uvicorn main:app --reload

