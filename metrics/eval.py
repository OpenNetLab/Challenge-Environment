#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse, json
from eval_video import VideoEvaluation, init_video_argparse, get_video_score
from eval_audio import AudioEvaluation, init_audio_argparse, get_audio_score, get_remote_ground
from eval_network import NetworkEvaluation, init_network_argparse, get_network_score


description = \
'''
This script provide multi methods to evaluate quality of video, audio and network.
'''

def init_argparse():
    video_parser = init_video_argparse()
    audio_parser = init_audio_argparse()
    network_parser = init_network_argparse()
    parser = argparse.ArgumentParser(description=description, parents=[video_parser, audio_parser, network_parser], conflict_handler='resolve')

    args = parser.parse_args()

    return args


if __name__ == "__main__":
    
    args = init_argparse()
    if args.scenario:
        args = get_remote_ground(args)
    
    out_dict = {}

    out_dict["video"] = get_video_score(args)
    out_dict["network"] = get_network_score(args)
    # We don't consider audio now. Give full score for the audio directly.
    out_dict["audio"] = 100.0
    # final_score = 0.2 * video + 0.1 * audio + (0.2 * delay_score + 0.2 * recv_rate_score + 0.3 * loss_score)
    # We don't consider audio now. Give full score for the audio directly.
    out_dict["final_score"] = 0.2 * out_dict["video"] + out_dict["network"] + 10
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))

