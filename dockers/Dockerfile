FROM alphartc:latest

RUN apt-get update && apt-get install -y \
    ffmpeg make nasm ninja-build doxygen python3-pip git
RUN pip3 install meson Cython

RUN git clone https://github.com/Netflix/vmaf.git
RUN cd vmaf && make install

COPY metrics /home/metrics