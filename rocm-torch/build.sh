#!/bin/bash

# FIX: assert /etc/timezone exist

docker build \
  --build-arg TZ=$(cat /etc/timezone) \
  --build-arg VIDEO_GID=$(getent group video | cut -d: -f3) \
  --build-arg RENDER_GID=$(getent group render | cut -d: -f3) \
  --build-arg USER_ID=$(id -u $USER) \
  --build-arg GROUP_ID=$(id -g $USER) \
  --label maintainer="WesleyCh3n" \
  -t asrock/asrock-translator:v1.0.0 .
