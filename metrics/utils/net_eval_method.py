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
    def __init__(self, delay_effect_interval=200):
        super(NetEvalMethodNormal, self).__init__()
        self.eval_name = "normal"
        self.delay_effect_interval = delay_effect_interval

    def eval(self, dst_audio_info : NetInfo):
        net_data = dst_audio_info.net_data
        ssrc_info = {}

        delay_list = []
        loss_count = 0
        self.last_seqNo = {}
        for item in net_data:
            ssrc = item["packetInfo"]["header"]["ssrc"]
            sequence_number = item["packetInfo"]["header"]["sequenceNumber"]
            tmp_delay = item["packetInfo"]["arrivalTimeMs"] - item["packetInfo"]["header"]["sendTimestamp"]
            if (ssrc not in ssrc_info):
                ssrc_info[ssrc] = {
                    "time_delta" : -tmp_delay,
                    "delay_list" : []
                }
            if ssrc in self.last_seqNo:
                loss_count += max(0, sequence_number - self.last_seqNo[ssrc] - 1)
            self.last_seqNo[ssrc] = sequence_number
                
            ssrc_info[ssrc]["delay_list"].append(ssrc_info[ssrc]["time_delta"] + tmp_delay)
        # scale delay list
        for ssrc in ssrc_info:
            min_delay = min(ssrc_info[ssrc]["delay_list"])
            # make offset if the first packet don't have the min delay
            base_delay = 0 if min_delay >= 0 else -min_delay
            mean_delay = np.mean(ssrc_info[ssrc]["delay_list"]) + base_delay
            max_delay = mean_delay + self.delay_effect_interval
            ssrc_info[ssrc]["scale_delay_list"] = [min(delay+base_delay, max_delay) / max_delay for delay in ssrc_info[ssrc]["delay_list"]]
        # delay score
        avg_delay_score = np.mean([np.mean(ssrc_info[ssrc]["scale_delay_list"]) for ssrc in ssrc_info])

        # higher loss rate, lower score
        avg_loss_rate = loss_count / (loss_count + len(net_data))

        # calculate result score and the score composition can be evenly divided into two parts
        avg_score = 50
        network_score = avg_score * (1 - avg_delay_score) + \
                            avg_score * (1 - avg_loss_rate)

        return network_score