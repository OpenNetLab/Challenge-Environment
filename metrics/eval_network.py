#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, argparse, json, shutil
import numpy as np
from utils.net_info import NetInfo
from utils.net_eval_method import NetEvalMethod, NetEvalMethodNormal


description = \
'''
This script provide multi methods to evaluate network quality.
'''


class NetworkEvaluation():
    def __init__(self, eval_method : NetEvalMethod, args):
        self.eval_method = eval_method
        self.args = args

    def eval(self, dst_network_path):
        dst_network_info = NetInfo(dst_network_path)
        ret = self.eval_method.eval(dst_network_info)

        return ret


def get_network_score(args):
    eval_method = None

    if args.network_eval_method == "normal":
        eval_method = NetEvalMethodNormal()
    else:
        raise ValueError("Not supoort such method to evaluate network")
    
    network_eval_tool = NetworkEvaluation(eval_method, args)
    network_out = network_eval_tool.eval(args.dst_network_log)

    return network_out


def init_network_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file. It will print the result in terminal if you don't specify its value.")
    # for network evaluation
    parser.add_argument("--network_eval_method", type=str, default="normal", choices=["normal"], help="the method to evaluate network.")
    parser.add_argument("--dst_network_log", type=str, required=True, default=None, help="the path of network log.")
    parser.add_argument("--delay_effect_interval", type=str, default="200", help="the effect interval of delay list. The delay out of this interval will be thought as bad performance.")

    return parser
    

if __name__ == "__main__":
    parser = init_network_argparse()
    args = parser.parse_args()
    out_dict = {}    
    out_dict["network"] = get_network_score(args)
        
    if args.output:
        with open(args.output, 'w') as f:
            f.write(json.dumps(out_dict))
    else:
        print(json.dumps(out_dict))
