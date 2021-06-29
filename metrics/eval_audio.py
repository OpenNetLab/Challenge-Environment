#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import subprocess, json, argparse, requests, os
from tempfile import NamedTemporaryFile
from utils.audio_info import AudioInfo
from utils.audio_eval_method import AudioEvalMethod, AudioEvalMethodDNSMOS


description = \
'''
This script provide multi methods to evaluate audio quality. 
For example, the method of DNSMOS https://github.com/microsoft/DNS-Challenge.
'''


class AudioEvaluation():
    def __init__(self, eval_method : AudioEvalMethod, args):
        self.eval_method = eval_method
        self.args = args

    def change_audio_config(self, audio_info : AudioInfo):
        if audio_info.sample_rate in self.eval_method.required_sample_rate and audio_info.channel in self.eval_method.required_channel:
            return None
        output = NamedTemporaryFile('w+t', suffix=".%s" % (audio_info.format_name))
        cmd = ["ffmpeg", "-i", audio_info.audio_path, "-ar", self.eval_method.required_sample_rate[0], \
                         "-ac", self.eval_method.required_channel[0], "-vn", "-y", output.name]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")

        return output

    def eval(self, dst_audio_path):
        dst_audio_info = AudioInfo(dst_audio_path)

        # check audio type
        fo_new_video = self.change_audio_config(dst_audio_info)
        dst_audio_info = AudioInfo(fo_new_video.name) if fo_new_video else dst_audio_info

        audio_score = self.eval_method.eval(dst_audio_info)
        # Use ground truth
        if self.args.ground_audio < 0:
            return audio_score
        
        return 100.0 if audio_score > self.args.ground_audio * self.args.binarize_bound else .0


def init_audio_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    parser.add_argument("--scenario", type=str, default=None, help="the name of scenario")
    parser.add_argument("--ground_service", type=str, default=None, help="the url where you want to get the score of ground truth")
    # for audio evaluation
    parser.add_argument("--audio_eval_method", type=str, default="dnsmos", choices=["dnsmos"], help="the method to evaluate audio, like DNSMOS")
    parser.add_argument("--dst_audio", type=str, default=None, required=True, help="the path of destination audio")
    parser.add_argument("--audio_sample_rate", type=str, default='16000', help="the sample rate of audio")
    parser.add_argument("--audio_channel", type=str, default='1', help="the numbers of audio channels")
    parser.add_argument("--ground_audio", type=float, default=-1, help="the audio score of a special scenario ground truth. -1 means not use ground")
    parser.add_argument("--binarize_bound", type=float, default=0.6, help="the bound to binarize audio score")
    # for DNSMOS
    parser.add_argument("--dnsmos_uri", type=str, default=None, help="the uri to evaluate audio provided by DNSMOS")
    parser.add_argument("--dnsmos_key", type=str, default=None, help="the key to evaluate audio provided by DNSMOS")

    return parser


def get_audio_score(args):
    eval_method = None

    if args.audio_eval_method == "dnsmos":
        eval_method = AudioEvalMethodDNSMOS(args.dnsmos_uri, args.dnsmos_key)
    else:
        raise ValueError("Not supoort such method to evaluate audio")
        
    audio_eval_tool = AudioEvaluation(eval_method, args)
    audio_out = audio_eval_tool.eval(args.dst_audio)

    return audio_out


def get_remote_ground(args):
    if args.ground_service[-4:] == "json":
        with NamedTemporaryFile('w+t') as f:
            cmd = ["wget", args.ground_service, "-O", f.name]
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            resp = f.read()
            if len(resp) == 0:
                raise ValueError("Error request to ground service %s" % (args.ground_service))
            resp = json.loads(resp)
        if args.scenario not in resp:
            raise ValueError("Not find scenario of %s" % (args.scenario))
        scenario_score = resp[args.scenario]
    else:
        resp = requests.get("http://%s/get_ground_truth/%s" % (args.ground_service, args.scenario)).text
        if len(resp) == 0:
            raise ValueError("Error request to ground service %s" % (args.ground_service))
        scenario_score = json.loads(resp)    

    if "ground_video" in args:
        args.ground_video = scenario_score["video"]
    if "ground_audio" in args:
        args.ground_audio = scenario_score["audio"]
    if "ground_recv_rate" in args:
        args.ground_recv_rate = scenario_score["recv_rate"]

    return args


if __name__ == "__main__":
    parser = init_audio_argparse()
    args = parser.parse_args()
    if args.scenario and args.ground_service:
        args = get_remote_ground(args)
    
    out_dict = {}
    out_dict["audio"] = get_audio_score(args)
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))