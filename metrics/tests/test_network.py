#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, json, subprocess
from tempfile import NamedTemporaryFile


cur_dir = os.path.dirname(os.path.abspath(__file__))


def check_network_score(dst_network_log):
    file_path = cur_dir + "/../eval_network.py"
    cmd = ["python3", file_path, "--network_eval_method", "normal", "--dst_network_log", dst_network_log]
    cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
    
    assert "network" in json.loads(cmd_result.stdout)

    # check output file
    with NamedTemporaryFile('w+t') as output:
        cmd.extend(["--output", output.name])
        cmd_result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")
        data = json.loads(output.read())
        assert "network" in data


def test_network_score():
    dst_network_log = cur_dir + "/data/alphartc.txt"
    check_network_score(dst_network_log)