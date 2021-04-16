import os, json, pytest


def test_dnsmos_audio(dnsmos_uri, dnsmos_key):
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = cur_dir + "/../metrics/eval.py"
    audio_path = cur_dir + "/data/test.wav"
    output = cur_dir + "/output.json"
    cmd = ["python3", file_path, "--dnsmos_uri", dnsmos_uri, "--dnsmos_key", dnsmos_key, "--dst_audio", audio_path, "--output", output]
    os.system(' '.join(cmd))
    with open(output, 'r') as f:
        data = json.loads(f.read())
    assert "audio" in data
