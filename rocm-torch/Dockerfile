FROM rocm/dev-ubuntu-24.04:6.2.1-complete

SHELL ["/usr/bin/bash", "-c"]

RUN apt-get update && \
  apt-get install --no-install-recommends -y git cmake python3-venv python3-dev && \
  apt-get clean && \
  rm -rf /var/lib/apt/lists/*

ARG USERNAME=asrocksw
ARG TZ
ARG VIDEO_GID
ARG RENDER_GID
# FIX: hard coded?
ENV AMDGPU_TARGETS="gfx1100"
ENV TZ=${TZ}

RUN userdel ubuntu \
  && adduser --disabled-password --gecos '' $USERNAME \
  && usermod -aG sudo $USERNAME \
  && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers \
  && if [[ "$VIDEO_GID" == "$(getent group video | cut -d: -f3)" ]]; then \
    usermod -aG video $USERNAME; \
  else \
    groupadd -g $VIDEO_GID video_map && usermod -aG video_map $USERNAME; \
  fi \
  && if [[ "$RENDER_GID" == "$(getent group render | cut -d: -f3)" ]]; then \
    usermod -aG render $USERNAME; \
  else \
    groupadd -g $RENDER_GID render_map && usermod -aG render_map $USERNAME; \
  fi

USER $USERNAME
WORKDIR /home/$USERNAME

ARG VENV_DIR=/home/$USERNAME/venv

COPY ./requirements.txt /tmp/
RUN python3 -m venv $VENV_DIR \
  && $VENV_DIR/bin/pip install --pre -r /tmp/requirements.txt \
  && find $VENV_DIR \( -type d -a -name test -o -name tests \) \
    -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
    -exec rm -rf '{}' \+ \
  && sudo rm /tmp/*
