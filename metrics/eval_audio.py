import argparse
import glob
import json
import os

import numpy as np
import pandas as pd
import requests
import soundfile as sf

from urllib.parse import urlparse, urljoin


class AudioEvaluation():
    def __init__(self, eval_method="dnsmos", eval_args=None):
        self.eval_method = eval_method
        self.eval_args = eval_args if eval_args else self.fill_default_args()

    def fill_default_args(self):
        if self.eval_method == "dnsmos":
            if "dnsmos_uri" not in self.eval_args or "dnsmos_key" not in self.eval_args:
                raise ValueError("Please provided the dns uri and key")
            self.audio_sample_rate = '16000'
            self.audio_channel = 1

    def change_audio_config(self, dst_audio_path, output=None):
        if not output:
            rel_path = dst_audio_path.split('/')[-1]
            output = dst_audio_path.replace(rel_path, "new_"+rel_path)
        cmd = ["ffmpeg -i", dst_audio_path, "-ar", self.eval_args["audio_sample_rate"], "-ac", self.eval_args["audio_channel"], \
                "-vn -y", output]
        os.system(' '.join(cmd))
        return output

    def eval_by_dnsmos(self, dst_audio_path):
        # Set the content type
        headers = {'Content-Type': 'application/json'}
        # If authentication is enabled, set the authorization header
        headers['Authorization'] = f'Basic {self.eval_args["dnsmos_key"] }'
        
        new_dst_audio_path = self.change_audio_config(dst_audio_path)
        
        audio, fs = sf.read(new_dst_audio_path)
        if fs != 16000:
            print('Only sampling rate of 16000 is supported as of now')
        data = {"data": audio.tolist()}
        input_data = json.dumps(data)
        # Make the request and display the response
        u = urlparse(self.eval_args["dnsmos_uri"])
        resp = requests.post(urljoin("https://" + u.netloc, 'score'), data=input_data, headers=headers)
        score_dict = resp.json()
        score_dict['file_name'] = os.path.basename(new_dst_audio_path)
        
        return score_dict["mos"]

    def eval(self, dst_audio_path):
        score_dict = {}

        if (self.eval_method == "dnsmos"):
            score_dict = self.eval_by_dnsmos(dst_audio_path)

        return score_dict
