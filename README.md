# Introduction 

The original intention of this project is to provide an evaluation standard for the OpenNetLab competition. The evaluation objects include video, audio and network.

- For video files, we use tools such as Vmaf to evaluate the quality of the video.
- For audio files, we use a method based on [Deep Noise Suppresiion](https://github.com/microsoft/DNS-Challenge) to evaluate the quality of the audio.

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:

## Installation process

Firstly, you should download our repository by running the order below :

```shell
git clone https://github.com/OpenNetLab/Challenge-Environment.git
```

Then, you can enter the directory of repository and contruct the environment by running the order below :

```shell
make all
```

Lastly, you will find that the image of Challenge-Environment is installed in your machine.

## Software dependencies

We provided the dockerfile to prepare the environment which have already installed all sofware dependencies. If you don't want to use docker, it is neccessary to install these software below :

|         | [ffmpeg](https://github.com/FFmpeg/FFmpeg) | [ffprobe](https://ffmpeg.org/ffprobe.html) | [Vmaf](https://github.com/Netflix/vmaf) | Python |
| :-----: | :----------------------------------------: | :----------------------------------------: | :-------------------------------------: | :----: |
| Version |                   4.3.2                    |                   4.3.2                    |                c8e367d8                 |  3.x   |

## Latest releases

## API references

We ingerated all metrics to a file `eval.py`. So you can just run the order below and get audio and video scores at the same time :

```shell
python3 eval.py --src_video {src_video} --dst_video {dst_video}  --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key} --output {output_file_path}
```

For the required arguments, you can find it and correspond description in [here](#Arguments Description).

We also support to evaluate video or audio separately. you can follow steps below to achieve this.

### For video evaluation

For the type of .mp4, .y4m, you can run order below yo get the vamp score of two videos quickly :

```shell
python3 evaluate_video.py --src_video {src_video_path} --dst_video {dst_video_path} --output {output_file_path}
```

For the required arguments, you can find it and correspond description in [here](#Arguments Description)

For the type of .yuv, you need to specify the optional arguments below :

- video_size : the size of video, like 1920x1080
- pixel_format : the pixel format of video, like  420, 422, 444
- bitdepth : the bitdepth of video, like 8, 10, 12

For more detail about the arguments, you can run order below to get description for video :

```shell
python3 evaluate_video.py -h
```

### For audio evaluation

For the type of .wav, you can run order below yo get the DNSMOS score of an audio quickly :

```shell
python3 eval_audio.py --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key} --output {output_file_path}
```

- dst_audio : the path of audio that you want to evaluate
- dnsmos_uri : the uri where you make request to 
- dnsmos_key : the key to check the right that you can use the API provided by dnsmos
- output : the path of output json file

For more detail about the arguments, you can run order below to get description for video :

```shell
python3 evaluate_audio.py -h
```

### Arguments Description

|   Arguments    |                         Description                          | eval.py | eval_video.py | eval_audio.py |
| :------------: | :----------------------------------------------------------: | :-----: | :-----------: | :-----------: |
| src_video_path |                   the path of source video                   | Sopport |    Sopport    |       \       |
| dst_video_path |                the path of destination video                 | Sopport |    Sopport    |       \       |
|     output     |                 the path of output json file                 | Sopport |    Sopport    |    Sopport    |
|   dst_audio    |         the path of audio that you want to evaluate          | Sopport |       \       |    Sopport    |
|   dnsmos_uri   |              the uri where you make request to               | Sopport |       \       |    Sopport    |
|   dnsmos_key   | the key to check the right that you can use the API provided by dnsmos | Sopport |       \       |    Sopport    |
|       -h       |               get more description of scripts                | Sopport |    Sopport    |    Sopport    |

# Build and Test

We run the tests based on the tools of pytest. So you can run the order below:
```shell
python3 -m pytest --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key}
```