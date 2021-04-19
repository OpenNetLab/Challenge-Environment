FROM alphartc:latest

# Add ONL user
ARG USER=onl

WORKDIR /home/${USER}

RUN apt-get update && apt-get install -y \
    ffmpeg make nasm ninja-build doxygen python3-pip git
RUN pip3 install meson Cython

RUN git clone https://github.com/Netflix/vmaf.git && cd vmaf && make -f Makefile install

COPY metrics metrics