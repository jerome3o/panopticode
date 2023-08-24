#!/bin/bash

# may be required: sudo docker login

# build
sudo docker build -t jerome3o/lights-server .

# publish
sudo docker push jerome3o/lights-server
