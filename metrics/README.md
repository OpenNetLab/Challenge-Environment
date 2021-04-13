# Introduction 
TODO: Give a short introduction of your project. Let this section explain the objectives or the motivation behind this project. 

The original intention of this project is to provide an evaluation standard for the OpenNetLab competition. The evaluation objects include video, audio and network.

- For video files, we use tools such as Vmaf to evaluate the quality of the video.
- For audio files, we use a method based on [Deep Noise Suppresiion](https://github.com/microsoft/DNS-Challenge) to evaluate the quality of the audio.

# Getting Started
TODO: Guide users through getting your code up and running on their own system. In this section you can talk about:

## Installation process

Just run the order by using git tools :

```shell
git clone https://OpenNetLab@dev.azure.com/OpenNetLab/ONL/_git/metrics
```

## Software dependencies

Because our evaluation method may rely on some open source projects and software. You need to make sure that these software have been installed before you use it.

|         | [ffmpeg](https://github.com/FFmpeg/FFmpeg) | [ffprobe](https://ffmpeg.org/ffprobe.html) | [Vmaf](https://github.com/Netflix/vmaf) | Python |
| :-----: | :----------------------------------------: | :----------------------------------------: | :-------------------------------------: | :----: |
| Version |                   4.3.2                    |                   4.3.2                    |                c8e367d8                 |  3.x   |

## Latest releases

## API references

### For video evaluation

For the type of .mp4, .y4m, you can run order below yo get the vamp score of two videos quickly :

```shell
python3 evaluate_video.py --src_video {src_video_path} --dst_video {dst_video_path}
```

- src_video_path : the path of source video
- dst_video_path : the path of destination video

For the type of .yuv, you need to specify the parameters below :

- video_size : the size of video, like 1920x1080
- pixel_format : the pixel format of video, like  420, 422, 444
- bitdepth : the bitdepth of video, like 8, 10, 12

For more detail about the arguments, you can run order below to get description for video :

```shell
python3 evaluate_video.py -h
```

### For audio evaluation

### For network evaluation

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)