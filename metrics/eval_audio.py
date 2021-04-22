#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
import os
from utils.audio_info import AudioInfo
from utils.audio_eval_method import AudioEvalMethod, AudioEvalMethodDNSMOS


description = \
'''
This file provide multi method to evaluate audio quality based on class of AudioEvalMethod. 
For example, the class of AudioEvalMethodDNSMOS inherit from AudioEvalMethod can evaluate audio quality by using DNSMO API.
'''


class AudioEvaluation():
    def __init__(self, eval_method : AudioEvalMethod, args):
        self.eval_method = eval_method
        self.args = args

    def eval(self, dst_audio_path):
        dst_audio_info = AudioInfo(dst_audio_path)

        score_dict = self.eval_method.eval(dst_audio_info)

        return score_dict


def init_audio_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for audio evaluation
    parser.add_argument("--audio_eval_method", type=str, default="dnsmos", help="the method to evaluate audio, like DNSMOS")
    parser.add_argument("--dst_audio", type=str, default=None, required=True, help="the path of destination audio")
    parser.add_argument("--audio_sample_rate", type=str, default='16000', help="the sample rate of audio")
    parser.add_argument("--audio_channel", type=str, default='1', help="the numbers of audio channels")
    # for DNSMOS
    parser.add_argument("--dnsmos_uri", type=str, default=None, help="the uri to evaluate audio provided by DNSMOS")
    parser.add_argument("--dnsmos_key", type=str, default=None, help="the key to evaluate audio provided by DNSMOS")

    return parser


def get_audio_score(eval_method, args):
    audio_eval_tool = AudioEvaluation(eval_method, args)
    audio_out = audio_eval_tool.eval(args.dst_audio)

    return audio_out


if __name__ == "__main__":
    parser = init_audio_argparse()
    args = parser.parse_args()
    out_dict = {}
    eval_method = None

    if (args.audio_eval_method == "dnsmos"):
        eval_method = AudioEvalMethodDNSMOS(args.dnsmos_uri, args.dnsmos_key)

    out_dict["audio"] = get_audio_score(eval_method, args)
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))