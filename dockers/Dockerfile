FROM alphartc:latest

# Add ONL user
ARG USER=onl

WORKDIR /home/${USER}

# Install dependency
RUN apt-get update && apt-get install -y \
    ffmpeg python3-pip wget unzip gocr imagemagick

RUN pip3 install pytest numpy requests soundfile

# Download release version of vmaf
RUN wget https://github.com/Netflix/vmaf/releases/download/v2.1.0/ubuntu-18.04-vmaf.zip
# Install vmaf
RUN unzip -o ubuntu-18.04-vmaf.zip && chmod 774 vmaf && mv vmaf /usr/bin && rm ubuntu-18.04-vmaf.zip

COPY metrics metrics

# OpenAI
RUN pip3 install gym
# PyTorch
RUN pip3 install torch
#Protobuf
RUN pip3 install protobuf==3.6.1
# TensorFlow
RUN pip3 install tensorflow==1.8.0

