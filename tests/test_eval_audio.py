#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, json, pytest


def get_audio_dnsmos(audio_path, dnsmos_uri, dnsmos_key, output):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval_audio.py"
    cmd = ["python3", file_path, "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "audio" in data


def test_dnsmos_audio(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    audio_path = cur_dir + "/data/test.wav"
    output = cur_dir + "/output.json"
    get_audio_dnsmos(audio_path, dnsmos_uri, dnsmos_key, output)
