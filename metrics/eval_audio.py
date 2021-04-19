#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import requests
import soundfile as sf

from urllib.parse import urlparse, urljoin


description = \
'''
Quickly Start:
python3 eval_audio.py --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key}
'''


class AudioEvaluation():
    def __init__(self, eval_method="dnsmos", eval_args=None):
        self.eval_method = eval_method
        self.eval_args = eval_args if eval_args else self.fill_default_args()

    def fill_default_args(self):
        if self.eval_method == "dnsmos":
            if "dnsmos_uri" not in self.eval_args or "dnsmos_key" not in self.eval_args:
                raise ValueError("Please provided the dns uri and key")
            self.audio_sample_rate = '16000'
            self.audio_channel = 1

    def change_audio_config(self, dst_audio_path, output=None):
        if not output:
            rel_path = dst_audio_path.split('/')[-1]
            output = dst_audio_path.replace(rel_path, "new_"+rel_path)
        cmd = ["ffmpeg -i", dst_audio_path, "-ar", self.eval_args["audio_sample_rate"], "-ac", self.eval_args["audio_channel"], \
                "-vn -y", output]
        os.system(' '.join(cmd))
        return output

    def eval_by_dnsmos(self, dst_audio_path):
        # Set the content type
        headers = {'Content-Type': 'application/json'}
        # If authentication is enabled, set the authorization header
        headers['Authorization'] = f'Basic {self.eval_args["dnsmos_key"] }'
        
        new_dst_audio_path = self.change_audio_config(dst_audio_path)
        
        audio, fs = sf.read(new_dst_audio_path)
        if fs != 16000:
            print('Only sampling rate of 16000 is supported as of now')
        data = {"data": audio.tolist()}
        input_data = json.dumps(data)
        # Make the request and display the response
        u = urlparse(self.eval_args["dnsmos_uri"])
        resp = requests.post(urljoin("https://" + u.netloc, 'score'), data=input_data, headers=headers)
        score_dict = resp.json()
        score_dict['file_name'] = os.path.basename(new_dst_audio_path)
        
        return score_dict["mos"]

    def eval(self, dst_audio_path):
        score_dict = {}

        if (self.eval_method == "dnsmos"):
            score_dict = self.eval_by_dnsmos(dst_audio_path)

        return score_dict


def init_audio_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for audio evaluation
    parser.add_argument("--audio_eval_method", type=str, default="dnsmos", help="the method to evaluate audio, like DNSMOS")
    parser.add_argument("--dst_audio", type=str, default=None, help="the path of destination audio")
    parser.add_argument("--audio_sample_rate", type=str, default='16000', help="the sample rate of audio")
    parser.add_argument("--audio_channel", type=str, default='1', help="the numbers of audio channels")
    # for DNSMOS
    parser.add_argument("--dnsmos_uri", type=str, default=None, help="the uri to evaluate audio provided by DNSMOS")
    parser.add_argument("--dnsmos_key", type=str, default=None, help="the key to evaluate audio provided by DNSMOS")

    return parser


def get_audio_score(args, eval_args):
    audio_eval_tool = AudioEvaluation(args.audio_eval_method, eval_args=eval_args)
    audio_out = audio_eval_tool.eval(args.dst_audio)
    return audio_out


def fill_audio_args(args):
    ret = {}
    if "dnsmos_uri" in args:
        ret["dnsmos_uri"] = args.dnsmos_uri
    if "dnsmos_key" in args:
        ret["dnsmos_key"] = args.dnsmos_key
    if "audio_sample_rate" in args:
        ret["audio_sample_rate"] = args.audio_sample_rate
    if "audio_channel" in args:
        ret["audio_channel"] = args.audio_channel

    return ret


if __name__ == "__main__":
    parser = init_audio_argparse()
    args = parser.parse_args()
    eval_args = fill_audio_args(args)
    out_dict = {}
    if (args.audio_eval_method == "dnsmos"):
        out_dict["audio"] = get_audio_score(args, eval_args)
        
    print(json.loads(json.dumps(out_dict)))
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))