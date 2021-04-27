#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))
file_path = cur_dir + "/../eval_video.py"


def check_video_vmaf(src_video, dst_video):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    
    data = json.loads(cmd_result.stdout)
    assert "video" in data
    assert type(data["video"]) == float
    
    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        
        data = json.loads(output.read())
        assert "video" in data
        assert type(data["video"]) == float 


def check_yuv_video_vmaf(src_video, dst_video, video_size, pixel_format, bitdepth):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    assert "video" in json.loads(cmd_result.stdout)
    
    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        data = json.loads(output.read())
        assert "video" in data


def test_y4m_y4m_compare():
    src_video = cur_dir + "/data/test.y4m"
    dst_video = cur_dir + "/data/test.y4m"
    check_video_vmaf(src_video, dst_video)


def test_y4m_yuv_compare():
    src_video = cur_dir + "/data/test.yuv"
    dst_video = cur_dir + "/data/test.y4m"
    check_video_vmaf(dst_video, src_video)
    check_video_vmaf(src_video, dst_video)

def test_yuv_yuv_compare():
    src_video = cur_dir + "/data/test.yuv"
    dst_video = cur_dir + "/data/test.yuv"
    check_yuv_video_vmaf(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8")