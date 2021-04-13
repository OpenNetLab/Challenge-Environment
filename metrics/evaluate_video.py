#!/usr/bin/env python3
# -*- coding: utf-8 -*-

description = \
'''
Quickly Start:
For the type of .mp4, y4m, just run "python3 evaluate_video.py --src_video {src_video_path} --dst_video {dst_video_path}"
'''

import os, sys, argparse


class VideoEvaluation():
    def __init__(self, eval_method="vmaf", eval_args=None):
        self.eval_method = eval_method
        self.eval_args = eval_args if eval_args else self.fill_default_args()

    def fill_default_args(self):
        eval_args = dict()
        if (self.eval_method == "vmaf"):
            eval_args["dst_video_type"] = ["y4m"]
            eval_args["output"] = "vmaf_output.xml"
        return eval_args

    def check_valid_of_path(self, path):
        return os.path.exists(path)

    def check_video_type(self, path):
        if ("dst_video_type" not in self.eval_args):
            return True
        return path.split('.')[-1] in self.eval_args["dst_video_type"]

    ### ffprobe orders below ###

    def get_video_info_by_ffprobe(self, path, output=None):
        if not output:
            output = "ffprobe.log"
        os.system("ffprobe -show_format %s  > ffprobe.log 2>&1" % (path))
        return output

    def get_video_fps_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "Stream" in x, f.readlines()))

        if not len(out):
            raise ValueError("Can not get the fps from %s by ffprobe." % (path))
        fps = list(filter(lambda x : "fps" in x, out[0].split(',')))[0].strip().split(' ')[0]
        return fps

    def get_video_dur_time_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "Duration" in x, f.readlines()))

        if not len(out):
            raise ValueError("Can not get the during time from %s by ffprobe." % (path))
        dur_time_stamp = list(filter(lambda x : "Duration" in x, out[0].split(',')))[0].strip().split(' ')[1].split(":")
        dur_time = float(dur_time_stamp[0])*3600 + float(dur_time_stamp[1])*60 + float(dur_time_stamp[2])
        return dur_time

    def get_video_size_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "fps" in x, f.readlines()))

        if not len(out):
            raise ValueError("Can not get the size from %s by ffprobe." % (path))
        video_size = list(filter(lambda x : "x" in x, out[0].split(',')))[1].strip().split('x')
        return video_size

    ### ffmpeg orders below ###

    def change_video_type(self, path, new_type, size=None):
        output = ''.join(path.split('.')[:-1]) + "." + new_type
        cmd = ["ffmpeg -i", path]
        if (not size):
            if ("video_size" in self.eval_args):
                size = self.eval_args["video_size"]
        if (size):
            if (type(size) == str):
                size = size.replace('X', 'x').split('x')
            if (type(size[0]) != str):
                size = list(map(lambda x : str(x), size))
            cmd.extend("-s %sx%s" % (size[0], size[1]))
        cmd.append(output)
        os.system(' '.join(cmd))
        return output

    def change_video_fps_by_ffmepg(self, path, fps, size=None, output=None):
        if not output:
            preffix, suffix = path.split('.')[:-1], path.split('.')[-1]
            output = ''.join(preffix) + '_%sfps.%s' % (fps, suffix)
        cmd = ["ffmpeg -i", path, "-r", str(fps)]
        if size and len(size) == 2:
            cmd.extend(["-s %sx%s" % (size[0], size[1])])
        cmd.append(output)
        os.system(' '.join(cmd))
        return output

    def frame_align_normal(self, src_video_path, dst_video_path):
        # Caculate the frame info by using ffprobe
        src_ffprobe_log_path = self.get_video_info_by_ffprobe(src_video_path)
        src_video_fps = float(self.get_video_fps_by_ffprobe(src_video_path, ffprobe_log=src_ffprobe_log_path))
        src_video_dur_time = self.get_video_dur_time_by_ffprobe(src_video_path, ffprobe_log=src_ffprobe_log_path)
        src_video_size = self.get_video_size_by_ffprobe(src_video_path, ffprobe_log=src_ffprobe_log_path)

        src_ffprobe_log_path = self.get_video_info_by_ffprobe(dst_video_path)
        dst_video_fps = float(self.get_video_fps_by_ffprobe(dst_video_path, ffprobe_log=src_ffprobe_log_path))
        dst_video_dur_time = float(self.get_video_dur_time_by_ffprobe(dst_video_path))
        
        # Frame alignment
        if (abs(src_video_dur_time*src_video_fps - dst_video_dur_time*dst_video_fps) >= 0.000001):
            new_fps = src_video_fps * src_video_dur_time / dst_video_dur_time
            new_dst_video_path = self.change_video_fps_by_ffmepg(dst_video_path, new_fps, src_video_size)
        else:
            new_dst_video_path = dst_video_path

        return new_dst_video_path

    def eval_by_vmaf(self, src_video_path, dst_video_path, size=None):            
        cmd = ["vmaf", "--reference", src_video_path, "--distorted", dst_video_path, "-m", "path=/home/vmaf/model/vmaf_v0.6.1.json"]
        if src_video_path.split('.')[-1] == "yuv":
            cmd.extend(["--width", size[0], "--height", size[1], \
                "--pixel_format", self.eval_args["pixel_format", "--bitdepth", self.eval_args["bitdepth"]]])
        if ("output" in self.eval_args):
            cmd.extend(["--output", self.eval_args["output"]])
        output_log = os.popen(' '.join(cmd)).read()
        # Todo : get log and return score

    def eval(self, src_video_path, dst_video_path):
        # Check the validity of the path
        if not self.check_valid_of_path(src_video_path):
            raise ValueError("The path of %s is invalid." % (src_video_path))
        if not self.check_valid_of_path(dst_video_path):
            raise ValueError("The path of %s is invalid." % (dst_video_path))
        # Check video type
        if not self.check_video_type(src_video_path):
            src_video_path = self.change_video_type(src_video_path, self.eval_args["dst_video_type"][0])
        if not self.check_video_type(dst_video_path):
            dst_video_path = self.change_video_type(dst_video_path, self.eval_args["dst_video_type"][0])

        if "video_size" in self.eval_args:
            video_size = self.eval_args["video_size"]  
        else:
            video_size =  self.get_video_size_by_ffprobe(src_video_path)

        if ("frame_align" in self.eval_args and self.eval_args["frame_align"] == "normal"):
            dst_video_path = self.frame_align_normal(src_video_path, dst_video_path)

        # Calculate video quality
        if self.eval_method == "vmaf":
            self.eval_by_vmaf(src_video_path, dst_video_path, video_size)


def init_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--method", type=str, default="vmaf", help="the method to evaluation, like vmaf")
    parser.add_argument("--src_video", type=str, default=None, help="the path of source video")
    parser.add_argument("--dst_video", type=str, default=None, help="the path of destination video")
    parser.add_argument("--frame_align", type=str, default="normal", help="how to do frame alignment")
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # required by the video format of yuv
    parser.add_argument("--video_size", type=str, default=None, help="the size of video, like 1920x1080.Required by the video format of yuv")
    parser.add_argument("--pixel_format", type=str, default=None, help="pixel format (420/422/444)")
    parser.add_argument("--bitdepth", type=str, default=None, help="bitdepth (8/10/12)")

    args = parser.parse_args()

    return args


def fill_args(args):
    ret = dict()
    if args.frame_align:
        ret["frame_align"] = args.frame_align
    if args.output:
        ret["output"] = args.output
    if args.video_size:
        ret["video_size"] = args.video_size
    if args.output:
        ret["pixel_format"] = args.pixel_format
    if args.video_size:
        ret["bitdepth"] = args.bitdepth

    return ret if len(ret) else None


if __name__ == "__main__":
    
    args = init_argparse()
    eval_args = fill_args(args)
    if (args.method == "vmaf"):
        video_eval_tool = VideoEvaluation(args.method, eval_args=eval_args)
        video_eval_tool.eval(args.src_video, args.dst_video)
    elif (args.mathod == "get_video_dur_time"):
        video_eval_tool = VideoEvaluation()
        video_eval_tool.get_video_dur_time_by_ffprobe(args.src_video)
