#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, json, shutil

sys.path.append(os.getcwd())

from metrics.eval_video import VideoEvaluation, init_video_argparse, fill_video_args, get_video_score
from metrics.eval_audio import AudioEvaluation, init_audio_argparse, fill_audio_args, get_audio_score


description = \
'''
Quickly Start:
python3 eval.py --src_video {src_video} --dst_video {dst_video}  --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key}
'''

def init_argparse():
    video_parser = init_video_argparse()
    audio_parser = init_audio_argparse()
    parser = argparse.ArgumentParser(description=description, parents=[video_parser, audio_parser], conflict_handler='resolve')
    parser.add_argument("--method", type=str, default="simple", help="the method to evaluation")
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for network evaluation
    parser.add_argument("--network_dir", type=str, default=None, help="the directory of network files")

    args = parser.parse_args()

    return args


def init_tmp_dir():
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    os.mkdir("tmp")


def fill_args(args):
    ret = {}
    video_ret = fill_video_args(args)
    audio_ret = fill_audio_args(args)
    ret.update(video_ret)
    ret.update(audio_ret)

    return ret


if __name__ == "__main__":
    
    args = init_argparse()
    eval_args = fill_args(args)
    init_tmp_dir()
    out_dict = {}
    if (args.method == "simple"):
        out_dict["video"] = get_video_score(args, eval_args)
        out_dict["audio"] = get_audio_score(args, eval_args)
        
    print(json.loads(json.dumps(out_dict)))
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))
    