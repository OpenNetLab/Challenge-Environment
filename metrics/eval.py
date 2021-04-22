#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, json, shutil

sys.path.append(os.getcwd())

from metrics.eval_video import VideoEvaluation, init_video_argparse, get_video_score
from metrics.eval_audio import AudioEvaluation, init_audio_argparse, get_audio_score
from metrics.eval_network import NetworkEvaluation, init_network_argparse, get_network_score


description = \
'''
Quickly Start:
This file provide multi method to evaluate quality of video, audio and network. 
You can find more informaiton form arguments -h.
'''

def init_argparse():
    video_parser = init_video_argparse()
    audio_parser = init_audio_argparse()
    network_parser = init_network_argparse()
    parser = argparse.ArgumentParser(description=description, parents=[video_parser, audio_parser, network_parser], conflict_handler='resolve')
    parser.add_argument("--method", type=str, default="simple", choices=["simple"], help="the method to evaluation")
    parser.add_argument("--output", type=str, default=None, help="the path of output file")

    args = parser.parse_args()

    return args

if __name__ == "__main__":
    
    args = init_argparse()
    out_dict = {}

    out_dict["video"] = get_video_score(args)
    out_dict["audio"] = get_audio_score(args)
    out_dict["network"] = get_network_score(args)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))
    