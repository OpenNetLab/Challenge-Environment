#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json


def get_network_score(dst_network_log, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval_network.py"
    cmd = ["python3", file_path, "--network_eval_method normal", "--dst_network_log", dst_network_log, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "network" in data


def test_network_score():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    output = cur_dir + "/output.json"
    dst_network_log = cur_dir + "/data/webrtc.log"
    get_network_score(dst_network_log, output)