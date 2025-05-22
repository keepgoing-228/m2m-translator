#!/bin/bash

docker run -it --rm \
  --device /dev/kfd \
  --device /dev/dri \
  --network host \
  --security-opt seccomp=unconfined \
  --cap-add=SYS_PTRACE \
  --ipc=host \
  -v $(pwd):/work/ \
  -v $HOME/.cache/huggingface:/home/asrocksw/.cache/huggingface \
  -w /work/ \
  -e HF_HOME="/home/asrocksw/.cache/huggingface" \
  -e HIP_VISIBLE_DEVICES="0,1" \
  --name m2m100-418m \
  asrock/asrock-translator:v1.0.0 \
  bash -c "source ~/venv/bin/activate && exec bash"
