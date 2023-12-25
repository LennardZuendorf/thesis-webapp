#!/bin/bash

# installing all the dependencies
pip install --no-cache-dir --upgrade -r requirements.txt

# running the fastapi app
uvicorn main:app --host 0.0.0.0 --port 8080
