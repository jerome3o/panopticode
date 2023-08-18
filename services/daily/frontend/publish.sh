#!/bin/bash

# get first arg as URL, if none then use default
URL=${1:-http://localhost:8000/}

# build
sudo docker build --build-arg URL=$URL -t jerome3o/daily-frontend .

# publish
sudo docker push jerome3o/daily-frontend
