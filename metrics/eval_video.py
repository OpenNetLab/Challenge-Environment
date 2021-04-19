#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, json, shutil


description = \
'''
Quickly Start:
python3 eval_video.py --src_video {src_video} --dst_video {dst_video} --output {output_path}
'''


class VideoEvaluation():
    def __init__(self, eval_method="vmaf", eval_args=None):
        self.eval_method = eval_method
        self.eval_args = self.fill_default_args()
        if eval_args:
            self.eval_args.update(eval_args)

    def fill_default_args(self):
        eval_args = dict()
        if (self.eval_method == "vmaf"):
            eval_args["dst_video_type"] = ["y4m"]
            eval_args["video_out"] = "tmp/vmaf_out.xml"
        return eval_args

    def check_valid_of_path(self, path):
        return os.path.exists(path)

    def check_video_type(self, path):
        if ("dst_video_type" not in self.eval_args):
            return True
        return path.split('.')[-1] in self.eval_args["dst_video_type"]

    ### ffprobe orders below ###
    def get_video_info_json(self, video_path):
        ffprobe_info = self.get_video_info_by_ffprobe(path)
        video_fps = self.get_video_fps_by_ffprobe(video_path, ffprobe_log=ffprobe_info)
        video_dur_time = self.get_video_dur_time_by_ffprobe(video_path, ffprobe_log=ffprobe_info)
        video_size = self.get_video_size_by_ffprobe(video_path, ffprobe_log=ffprobe_info)

        ret = {}
        ret["video_fps"] = video_fps
        ret["video_dur_time"] = video_dur_time
        ret["video_size"] = video_size

        return ret

    def get_video_info_by_ffprobe(self, path, output=None):
        if not output:
            output = "tmp/ffprobe.log"
        cmd = ["ffprobe -show_format", path]
        if "video_size" in self.eval_args and self.eval_args["video_size"]:
            cmd.extend(["-video_size %sx%s" % (self.eval_args["video_size"][0], self.eval_args["video_size"][0][1])])
        cmd.extend([">", output, "2>&1"])
        os.system(' '.join(cmd))

        return output

    def get_video_fps_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "Stream" in x, f.readlines()))

        if not len(out):
            # raise ValueError("Can not get the fps from %s by ffprobe." % (path))
            return None
        fps = list(filter(lambda x : "fps" in x, out[0].split(',')))[0].strip().split(' ')[0]
        return fps

    def get_video_dur_time_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "Duration" in x, f.readlines()))

        if not len(out):
            # raise ValueError("Can not get the during time from %s by ffprobe." % (path))
            return None
        dur_time_stamp = list(filter(lambda x : "Duration" in x, out[0].split(',')))[0].strip().split(' ')[1].split(":")
        dur_time = float(dur_time_stamp[0])*3600 + float(dur_time_stamp[1])*60 + float(dur_time_stamp[2])
        return dur_time

    def get_video_size_by_ffprobe(self, path, ffprobe_log=None):
        ffprobe_log = ffprobe_log if ffprobe_log else self.get_video_info_by_ffprobe(path)
        with open(ffprobe_log, 'r') as f:
            out = list(filter(lambda x : "fps" in x, f.readlines()))

        if not len(out):
            # raise ValueError("Can not get the size from %s by ffprobe." % (path))
            return None
        video_size = list(filter(lambda x : "x" in x, out[0].split(',')))[1].strip().split('x')
        return video_size

    ### ffmpeg orders below ###

    def change_video_type(self, path, new_type, size=None):
        output = "tmp/new_" + path.split('/')[-1].split('.')[0] + '.%s' % new_type
        print(output)
        # output = ''.join(path.split('.')[:-1]) + "." + new_type
        cmd = ["ffmpeg"]
        if (not size):
            if ("video_size" in self.eval_args):
                size = self.eval_args["video_size"]
        if (size):
            if (type(size) == str):
                size = size.replace('X', 'x').split('x')
            if (type(size[0]) != str):
                size = list(map(lambda x : str(x), size))
            cmd.append("-video_size %sx%s" % (size[0], size[1]))
        cmd.extend(["-i", path])
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
        src_video_info = self.get_video_info_json(src_video_path)
        dst_video_info = self.get_video_info_json(dst_video_info)

        if "video_fps" not in self.eval_args:
            self.eval_args["video_fps"] = src_video_info["video_fps"] if src_video_info["video_fps"] else dst_video_info["video_fps"]
        if "video_dur_time" not in self.eval_args:
            self.eval_args["video_dur_time"] = src_video_info["video_dur_time"] if src_video_info["video_dur_time"] else dst_video_info["video_dur_time"]
        if "video_size" not in self.eval_args:
            self.eval_args["video_size"] = src_video_info["video_size"] if src_video_info["video_size"] else dst_video_info["video_size"]
        
        # Frame alignment
        if (abs(src_video_dur_time*src_video_fps - dst_video_dur_time*dst_video_fps) >= 0.000001):
            new_fps = dst_video_fps * dst_video_dur_time / src_video_dur_time
            new_src_video_path = self.change_video_fps_by_ffmepg(src_video_path, new_fps, self.eval_args["video_size"])
        else:
            new_src_video_path = dst_video_path

        return new_src_video_path

    def eval_by_vmaf(self, src_video_path, dst_video_path, size=None):            
        cmd = ["vmaf", "--reference", src_video_path, "--distorted", dst_video_path]
        if src_video_path.split('.')[-1] == "yuv":
            cmd.extend(["--width", size[0], "--height", size[1], \
                "--pixel_format", self.eval_args["pixel_format", "--bitdepth", self.eval_args["bitdepth"]]])
        cmd.extend(["--output", self.eval_args["video_out"]])
        os.system(' '.join(cmd))
        with open(self.eval_args["video_out"], 'r') as f:
            vmaf_score_line = list(filter(lambda x : "metric" in x and "vmaf" in x, f.readlines()))
            vmaf_score = list(filter(lambda x : "mean" in x, vmaf_score_line[0].split(' ')))[0].split('=')[-1][1:-1]

        return vmaf_score

    def eval(self, src_video_path, dst_video_path):
        # Check the validity of the path
        if not self.check_valid_of_path(src_video_path):
            raise ValueError("The path of %s is invalid." % (src_video_path))
        if not self.check_valid_of_path(dst_video_path):
            raise ValueError("The path of %s is invalid." % (dst_video_path))
        # init video size
        if not self.eval_args["video_size"]:
            self.eval_args["video_size"] =  self.get_video_size_by_ffprobe(dst_video_path)
            if not self.eval_args["video_size"]:
                self.eval_args["video_size"] =  self.get_video_size_by_ffprobe(src_video_path)
        # Check video type
        if not self.check_video_type(src_video_path):
            src_video_path = self.change_video_type(src_video_path, self.eval_args["dst_video_type"][0])
        if not self.check_video_type(dst_video_path):
            dst_video_path = self.change_video_type(dst_video_path, self.eval_args["dst_video_type"][0])

        if ("frame_align" in self.eval_args and self.eval_args["frame_align"] == "normal"):
            src_video_path = self.frame_align_normal(src_video_path, dst_video_path)

        ret = 0
        # Calculate video quality
        if self.eval_method == "vmaf":
            ret = self.eval_by_vmaf(src_video_path, dst_video_path, self.eval_args["video_size"]  )

        return ret


def get_video_score(args, eval_args):
    video_eval_tool = VideoEvaluation(args.video_eval_method, eval_args=eval_args)
    video_out = video_eval_tool.eval(args.src_video, args.dst_video)
    return video_out


def init_video_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for video evaluation
    parser.add_argument("--video_eval_method", type=str, default="vmaf", help="the method to evaluate video, like vmaf")
    parser.add_argument("--src_video", type=str, default=None, help="the path of source video")
    parser.add_argument("--dst_video", type=str, default=None, help="the path of destination video")
    parser.add_argument("--frame_align", type=str, default="ffmpeg", help="how to do frame alignment")
    # required by the video format of yuv raw video
    parser.add_argument("--video_size", type=str, default=None, help="the size of video, like 1920x1080.Required by the video format of yuv")
    parser.add_argument("--pixel_format", type=str, default=None, help="pixel format (420/422/444)")
    parser.add_argument("--bitdepth", type=str, default=None, help="bitdepth (8/10/12)")

    return parser


def init_tmp_dir():
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    os.mkdir("tmp")


def fill_video_args(args):
    ret = dict()
    ret["frame_align"] = args.frame_align
    ret["output"] = args.output
    ret["video_size"] = args.video_size
    ret["pixel_format"] = args.pixel_format
    ret["bitdepth"] = args.bitdepth

    return ret if len(ret) else None


if __name__ == "__main__":
    parser = init_video_argparse()
    args = parser.parse_args()
    eval_args = fill_video_args(args)
    init_tmp_dir()
    out_dict = {}
    if (args.video_eval_method == "vmaf"):
        out_dict["video"] = get_video_score(args, eval_args)
        
    print(out_dict)
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))
