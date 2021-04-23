FROM alphartc:latest

# Add ONL user
ARG USER=onl

WORKDIR /home/${USER}

# VMAF
RUN apt-get update && apt-get install -y \
    ffmpeg make nasm ninja-build doxygen python3-pip git xxd

RUN pip3 install meson Cython pytest numpy requests soundfile

RUN git clone https://github.com/Netflix/vmaf.git && cd vmaf && make all && make install

COPY metrics metrics

# OpenAI
RUN pip3 install gym
# PyTorch
RUN pip3 install torch
# TensorFlow
RUN pip3 install tensorflow

