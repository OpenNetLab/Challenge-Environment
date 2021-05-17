#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, subprocess
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))
file_path = cur_dir + "/../eval_video.py"


def run_and_check_result(cmd):
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    
    data = json.loads(cmd_result.stdout)
    assert "video" in data
    assert type(data["video"]) == float
    assert data["video"] >= 0 and data["video"] <= 100

    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")

        data = json.loads(output.read())
        assert "video" in data
        assert type(data["video"]) == float 
        assert data["video"] >= 0 and data["video"] <= 100


def check_video_vmaf(src_video, dst_video):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video]
    
    run_and_check_result(cmd)


def check_yuv_video_vmaf(src_video, dst_video, video_size, pixel_format, bitdepth):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video, \
                                 "--video_size", video_size, "--pixel_format", pixel_format, "--bitdepth", bitdepth]
    run_and_check_result(cmd)


def check_ocr_video_vmaf(src_video, dst_video, align_method):
    cmd = ["python3", file_path, "--video_eval_method", "vmaf", "--src_video", src_video, "--dst_video", dst_video]
    if align_method:
        cmd.extend(["--frame_align_method", align_method])
    
    run_and_check_result(cmd)


def test_y4m_yuv_compare(y4m_video, yuv_video):
    src_video = y4m_video
    dst_video = yuv_video
    check_video_vmaf(dst_video, src_video)
    check_video_vmaf(src_video, dst_video)

def test_yuv_yuv_compare(yuv_video):
    src_video = yuv_video
    dst_video = yuv_video
    check_yuv_video_vmaf(dst_video, src_video, video_size="320x240", pixel_format="420", bitdepth="8")


def test_y4m_align_compare(y4m_video, align_method):
    src_video = y4m_video
    dst_video = y4m_video
    check_ocr_video_vmaf(src_video, dst_video, align_method)