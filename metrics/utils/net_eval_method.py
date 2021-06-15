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
    def __init__(self, max_delay=400, ground_recv_rate=500):
        super(NetEvalMethodNormal, self).__init__()
        self.eval_name = "normal"
        self.max_delay = max_delay
        self.ground_recv_rate = ground_recv_rate

    def eval(self, dst_audio_info : NetInfo):
        net_data = dst_audio_info.net_data
        ssrc_info = {}

        delay_list = []
        for item in net_data:
            ssrc = item["packetInfo"]["header"]["ssrc"]
            tmp_delay = item["packetInfo"]["arrivalTimeMs"] - item["packetInfo"]["header"]["sendTimestamp"]
            if (ssrc not in ssrc_info):
                ssrc_info[ssrc] = {
                    "time_delta" : -tmp_delay,
                    "delay_list" : [],
                    "received_nbytes" : 0,
                    "start_recv_time" : item["packetInfo"]["arrivalTimeMs"],
                    "avg_recv_rate" : 0
                }
                
            ssrc_info[ssrc]["delay_list"].append(ssrc_info[ssrc]["time_delta"] + tmp_delay)
            ssrc_info[ssrc]["received_nbytes"] += item["packetInfo"]["payloadSize"]
            if item["packetInfo"]["arrivalTimeMs"] != ssrc_info[ssrc]["start_recv_time"]:
                ssrc_info[ssrc]["avg_recv_rate"] = ssrc_info[ssrc]["received_nbytes"] / (item["packetInfo"]["arrivalTimeMs"] - ssrc_info[ssrc]["start_recv_time"])
            
        # scale delay list
        for ssrc in ssrc_info:
            min_delay = min(ssrc_info[ssrc]["delay_list"])
            ssrc_info[ssrc]["scale_delay_list"] = [min(self.max_delay, delay) for delay in ssrc_info[ssrc]["delay_list"]]
            delay_pencentile_95 = np.percentile(ssrc_info[ssrc]["scale_delay_list"], 95)
            ssrc_info[ssrc]["delay_score"] = (self.max_delay - delay_pencentile_95) / (self.max_delay - min_delay / 2)
        # delay score
        avg_delay_score = np.mean([np.mean(ssrc_info[ssrc]["delay_score"]) for ssrc in ssrc_info])

        # receive rate score
        recv_rate_list = [ssrc_info[ssrc]["avg_recv_rate"] for ssrc in ssrc_info if ssrc_info[ssrc]["avg_recv_rate"] > 0]
        avg_recv_rate_score = np.mean(recv_rate_list) / self.ground_recv_rate

        # higher loss rate, lower score
        loss_list = [item["packetInfo"]["lossRates"] for item in net_data]
        avg_loss_rate = sum(loss_list) / len(net_data)

        # calculate result score
        network_score = 100 * 0.2 * avg_delay_score + \
                            100 * 0.2 * avg_recv_rate_score + \
                            100 * 0.3 * (1 - avg_loss_rate)

        return network_score