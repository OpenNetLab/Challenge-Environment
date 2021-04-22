#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))
file_path = cur_dir + "/../eval.py"


def get_score(src_video, dst_video, audio_path, dnsmos_uri, dnsmos_key, dst_network_log):
    cmd = ["python3", file_path, "--method", "simple", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, \
                                 "--dst_network_log", dst_network_log]

    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    data = json.loads(cmd_result.stdout)
    assert "video" in data
    assert "audio" in data
    assert "network" in data

    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        data = json.loads(output.read())
        assert "video" in data
        assert "audio" in data
        assert "network" in data


def get_yuv_score(src_video, dst_video, video_size, pixel_format, bitdepth, audio_path, dnsmos_uri, dnsmos_key, dst_network_log):
    cmd = ["python3", file_path, "--method", "simple", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth, \
                                 "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, \
                                 "--dst_network_log", dst_network_log]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    data = json.loads(cmd_result.stdout)
    assert "video" in data
    assert "audio" in data
    assert "network" in data

    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        data = json.loads(output.read())
        assert "video" in data
        assert "audio" in data
        assert "network" in data


def test_y4m_score(dnsmos_uri, dnsmos_key):
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.y4m"
    dst_video = cur_dir + "/data/horse.y4m"
    audio_path = cur_dir + "/data/test.wav"
    dst_network_log = cur_dir + "/data/webrtc.out"
    get_score(src_video, dst_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, dst_network_log=dst_network_log)


def test_yuv_vmaf(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.y4m"
    audio_path = cur_dir + "/data/test.wav"
    dst_network_log = cur_dir + "/data/webrtc.out"
    get_score(dst_video, src_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, dst_network_log=dst_network_log)
    get_score(src_video, dst_video, audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, dst_network_log=dst_network_log)


def test_yuv_input_score(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    src_video = cur_dir + "/data/horse.yuv"
    dst_video = cur_dir + "/data/horse.yuv"
    audio_path = cur_dir + "/data/test.wav"
    dst_network_log = cur_dir + "/data/webrtc.out"
    get_yuv_score(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8", \
                        audio_path=audio_path, dnsmos_uri=dnsmos_uri, dnsmos_key=dnsmos_key, dst_network_log=dst_network_log)
