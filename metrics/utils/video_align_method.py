#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess
from tempfile import NamedTemporaryFile
from utils.video_info import VideoInfo


class VideoAlignMethod(object):
    def __init__(self):
        self.align_method_name = "base"

    def frame_align(self, src_video_info : VideoInfo, dst_video_info : VideoInfo):
        pass


class VideoAlignMethodFfmpeg(VideoAlignMethod):
    def __init__(self):
        super(VideoAlignMethodFfmpeg, self).__init__()
        self.align_method_name = "ffmpeg"

    def change_video_fps_by_ffmepg(self, video_info : VideoInfo, fps : int):
        output = NamedTemporaryFile('w+t', suffix=".%s" % (video_info.format_abbreviation))
        cmd = ["ffmpeg", "-i", video_info.video_path, "-r", str(fps), "-y"]
        if video_info.video_size:
            cmd.extend(["-s", video_info.video_size])
        cmd.append(output.name)
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        return output

    def frame_align(self, src_video_info : VideoInfo, dst_video_info : VideoInfo):

        fp_new_video = None
        # Frame alignment
        if not src_video_info.fps or \
                abs(src_video_info.get_frame_count() - dst_video_info.get_frame_count()) >= 0.000001:
            new_fps = dst_video_info.get_frame_count() / float(src_video_info.duration_sec)
            fp_new_video = self.change_video_fps_by_ffmepg(src_video_info, new_fps)

        return fp_new_video
