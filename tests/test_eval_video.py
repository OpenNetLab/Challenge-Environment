#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, pytest


def get_video_vmaf(src_video, dst_video, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval_video.py"
    cmd = ["python3", file_path, "--video_eval_method vmaf", "--src_video", src_video, "--dst_video", dst_video, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def get_yuv_video_vmaf(src_video, dst_video, video_size, pixel_format, bitdepth, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval_video.py"
    cmd = ["python3", file_path, "--video_eval_method vmaf", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def test_y4m_vmaf():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.y4m"
    dst_video = cur_dir + "/data/horse.y4m"
    get_video_vmaf(src_video, dst_video, output)


def test_yuv_vmaf():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.y4m"
    get_video_vmaf(dst_video, src_video, output)
    get_video_vmaf(src_video, dst_video, output)

def test_yuv_input_vmaf():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.yuv"
    get_yuv_video_vmaf(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8", output=output)