#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, sys, argparse, json, shutil
import numpy as np


description = \
'''
Quickly Start:
python3 eval_network.py --dst_network_log {dst_network_log}å --output {output_path}
'''


class NetworkEvaluation():
    def __init__(self, eval_method="normal", eval_args=None):
        self.eval_method = eval_method
        self.eval_args = self.fill_default_args()
        if eval_args:
            self.eval_args.update(eval_args)

    def fill_default_args(self):
        eval_args = dict()
        return eval_args

    def check_valid_of_path(self, path):
        return os.path.exists(path)

    def get_json_from_raw(self, dst_network_path):
        ret = []
        with open(dst_network_path, 'r') as f:
            for line in f.readlines():
                if ("remote_estimator_proxy.cc" not in line):
                    continue
                try:
                    raw_json = line[line.index('{'):]
                    json_network = json.loads(raw_json)
                    # it seems no use
                    del json_network["mediaInfo"]
                    ret.append(json_network)
                # can not parser json
                except ValueError as e:
                    pass
                # other exception that need to care
                except Exception as e:
                    print(e)
                    raise ValueError("Exception when parser json log")
        return ret

    def eval_by_normal(self, dst_network_path):
        clear_data = self.get_json_from_raw(dst_network_path)
        ssrc_info = {}

        jitter_list = []
        for item in clear_data:
            ssrc = item["packetInfo"]["header"]["ssrc"]
            tmp_delay = item["packetInfo"]["arrivalTimeMs"] - item["packetInfo"]["header"]["sendTimestamp"]
            if (ssrc not in ssrc_info):
                ssrc_info[ssrc] = {
                    "pkt_size_list" : []
                }
                ssrc_info[ssrc]["base_arrivalTimeMs"] = item["packetInfo"]["arrivalTimeMs"] 
                ssrc_info[ssrc]["base_sendTimestamp"] = item["packetInfo"]["header"]["sendTimestamp"]
                ssrc_info[ssrc]["base_delay"] = tmp_delay
            else:
                jitter_list.append(tmp_delay - ssrc_info[ssrc]["base_delay"])

            ssrc_info[ssrc]["last_arrivalTimeMs"] = item["packetInfo"]["arrivalTimeMs"] 
            ssrc_info[ssrc]["last_sendTimestamp"] = item["packetInfo"]["header"]["sendTimestamp"]
            ssrc_info[ssrc]["pkt_size_list"].append(item["packetInfo"]["header"]["headerLength"] + item["packetInfo"]["payloadSize"])
        
        # higher jitter variance, lower score
        jitter_var = np.std(jitter_list)

        # higher loss rate, lower score
        loss_list = [item["packetInfo"]["lossRates"] for item in clear_data]
        avg_loss_rate = sum(loss_list) / len(clear_data)

        avg_throughput_bps_list = [sum(ssrc_info[k]["pkt_size_list"]) * 8 / 
                                    (ssrc_info[k]["last_arrivalTimeMs"] - ssrc_info[k]["base_arrivalTimeMs"]) * 1e3 for k in ssrc_info]
        # stardard throughput by using the max value
        throughput_score_rate = np.mean(list(map(lambda x : x / max(avg_throughput_bps_list), avg_throughput_bps_list)))

        # calculate result score and the score composition can be evenly divided into three parts
        avg_score = 100 / 3
        network_score = avg_score - min(avg_score, jitter_var) + \
                            avg_score * (1 - avg_loss_rate) + \
                            avg_score * throughput_score_rate

        return network_score


    def eval(self, dst_network_path):
        # Check the validity of the path
        if not self.check_valid_of_path(dst_network_path):
            raise ValueError("The path of %s is invalid." % (dst_network_path))

        if self.eval_method == "normal":
            ret = self.eval_by_normal(dst_network_path)

        return ret


def get_network_score(args, eval_args):
    network_eval_tool = NetworkEvaluation(args.network_eval_method, eval_args=eval_args)
    network_out = network_eval_tool.eval(args.dst_network_log)
    return network_out


def init_network_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for network evaluation
    parser.add_argument("--network_eval_method", type=str, default="normal", help="the method to evaluate network")
    parser.add_argument("--dst_network_log", type=str, default=None, help="the path of network log")

    return parser


def fill_network_args(args):
    ret = dict()

    return ret if len(ret) else None


if __name__ == "__main__":
    parser = init_network_argparse()
    args = parser.parse_args()
    eval_args = fill_network_args(args)
    out_dict = {}
    if (args.network_eval_method == "normal"):
        out_dict["network"] = get_network_score(args, eval_args)
        
    print(json.loads(json.dumps(out_dict)))
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))
