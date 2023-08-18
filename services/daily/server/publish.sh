#!/bin/bash

# may be required: sudo docker login

# build
sudo docker build --build-arg URL=$URL -t jerome3o/daily-server .

# publish
sudo docker push jerome3o/daily-server
