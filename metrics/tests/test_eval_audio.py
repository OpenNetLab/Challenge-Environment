#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, pytest, subprocess
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))


def check_audio_dnsmos(audio_path, dnsmos_uri, dnsmos_key):
    file_path = cur_dir + "/../eval_audio.py"
    cmd = ["python3", file_path, "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")

    assert "audio" in json.loads(cmd_result.stdout)
    
    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        data = json.loads(output.read())
        assert "audio" in data


def test_dnsmos_audio(dnsmos_uri, dnsmos_key):
    audio_path = cur_dir + "/data/test.wav"
    check_audio_dnsmos(audio_path, dnsmos_uri, dnsmos_key)
