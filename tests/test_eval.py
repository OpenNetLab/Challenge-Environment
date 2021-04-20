#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, pytest


def get_video_vmaf(src_video, dst_video, audio_path, dnsmos_uri, dnsmos_key, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval.py"
    cmd = ["python3", file_path, "--method simple", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def get_yuv_video_vmaf(src_video, dst_video, video_size, pixel_format, bitdepth, audio_path, dnsmos_uri, dnsmos_key, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval.py"
    cmd = ["python3", file_path, "--method simple", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth, \
                                 "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def test_y4m_vmaf(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.y4m"
    dst_video = cur_dir + "/data/horse.y4m"
    audio_path = cur_dir + "/data/test.wav"
    get_video_vmaf(src_video, dst_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, output=output)


def test_yuv_vmaf(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.y4m"
    audio_path = cur_dir + "/data/test.wav"
    get_video_vmaf(dst_video, src_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, output=output)
    get_video_vmaf(src_video, dst_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, output=output)

def test_yuv_input_vmaf(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.yuv"
    audio_path = cur_dir + "/data/test.wav"
    get_yuv_video_vmaf(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8", \
                        audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, output=output)
