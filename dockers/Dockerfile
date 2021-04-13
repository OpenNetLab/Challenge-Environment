FROM alphartc:latest

RUN apt-get update && apt-get install -y \
    ffmpeg make nasm ninja-build doxygen python3-pip

RUN pip3 install meson Cython

COPY vmaf /home/vmaf
COPY metrics /home/metrics