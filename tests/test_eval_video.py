#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess


cur_dir = os.path.dirname(os.path.abspath(__file__))
file_path = cur_dir + "/../metrics/eval_video.py"
output = cur_dir + "/output.json"


def check_video_vmaf(src_video, dst_video, output):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    assert "video" in json.loads(cmd_result.stdout)
    
    # check output file
    cmd.extend(["--output", output])
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def check_yuv_video_vmaf(src_video, dst_video, video_size, pixel_format, bitdepth, output):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    assert "video" in json.loads(cmd_result.stdout)
    
    # check output file
    cmd.extend(["--output", output])
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "video" in data


def test_y4m_y4m_compare():
    src_video = cur_dir + "/data/test.y4m"
    dst_video = cur_dir + "/data/test.y4m"
    check_video_vmaf(src_video, dst_video, output)


def test_y4m_yuv_compare():
    src_video = cur_dir + "/data/test.yuv"
    dst_video = cur_dir + "/data/test.y4m"
    check_video_vmaf(dst_video, src_video, output)
    check_video_vmaf(src_video, dst_video, output)

def test_yuv_yuv_compare():
    src_video = cur_dir + "/data/test.yuv"
    dst_video = cur_dir + "/data/test.yuv"
    check_yuv_video_vmaf(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8", output=output)