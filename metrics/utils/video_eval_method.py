#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, tempfile, re, os
from utils.video_info import VideoInfo
from tempfile import NamedTemporaryFile


class VideoEvalMethod(object):
    def __init__(self):
        self.method_name = "base"
        self.support_type = []
        self.support_type_abbreviation = []

    def eval(self, src_video_info : VideoInfo, dst_video_info : VideoInfo):  
        pass


class VideoEvalMethodVmaf(VideoEvalMethod):
    def __init__(self, model_path=None):
        super(VideoEvalMethodVmaf, self).__init__()
        self.method_name = "ffmpeg"
        self.support_type = ["yuv4mpegpipe", "rawvideo"]
        self.support_type_abbreviation = ["y4m", "yuv"]
        if model_path:
            self.model_path = model_path
        elif os.path.exist("/home/onl/vmaf/model/vmaf_v0.6.1.json"):
            self.model_path = "/home/onl/vmaf/model/vmaf_v0.6.1.json"

    def eval(self, src_video_info : VideoInfo, dst_video_info : VideoInfo):  
        if src_video_info.format_name != dst_video_info.format_name:
            raise ValueError("Can't compare bewteen different video type")
        if src_video_info.format_name not in self.support_type:
            raise ValueError("Video type don't support")

        cmd = ["vmaf", "--reference", src_video_info.video_path, "--distorted", dst_video_info.video_path]
        if self.model_path:
            cmd.extend(["-m", "path=%s" % (self.model_path)])

        if src_video_info.format_name == "rawvideo":
            cmd.extend(["--width", src_video_info.width, "--height", src_video_info.height, \
                "--pixel_format", src_video_info.pixel_format, "--bitdepth", src_video_info.bitdepth])
        
        with NamedTemporaryFile('w+t', suffix=".xml") as f:
            cmd.extend(["--output", f.name])
            cmd_result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
            vmaf_score = re.search(r'metric name="vmaf".*?mean="([\d]+\.[\d]+)"', f.read()).group(1)

        return vmaf_score
