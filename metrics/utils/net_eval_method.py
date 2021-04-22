#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from utils.net_info import NetInfo
import numpy as np
from abc import ABC, abstractmethod


class NetEvalMethod(ABC):
    @abstractmethod
    def __init__(self):
        self.eval_name = "base"

    @abstractmethod
    def eval(self, dst_audio_info : NetInfo):
        pass


class NetEvalMethodNormal(NetEvalMethod):
    def __init__(self):
        super(NetEvalMethodNormal, self).__init__()
        self.eval_name = "normal"

    def eval(self, dst_audio_info : NetInfo):
        net_data = dst_audio_info.net_data
        ssrc_info = {}

        jitter_list = []
        for item in net_data:
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
        loss_list = [item["packetInfo"]["lossRates"] for item in net_data]
        avg_loss_rate = sum(loss_list) / len(net_data)

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