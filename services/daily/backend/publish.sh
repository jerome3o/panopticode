#!/bin/bash

# may be required: sudo docker login

# build
sudo docker build -t jerome3o/daily-backend .

# publish
sudo docker push jerome3o/daily-backend
