#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests, subprocess, glob, json
import soundfile as sf
from utils.audio_info import AudioInfo
from urllib.parse import urlparse, urljoin
from tempfile import NamedTemporaryFile


class AudioEvalMethod(object):
    def __init__(self):
        self.eval_name = "base"
        self.required_sample_rate = []
        self.required_channel = []

    def eval(self, dst_audio_info : AudioInfo):
        pass


class AudioEvalMethodDNSMOS(AudioEvalMethod):
    def __init__(self, dnsmos_uri, dnsmos_key):
        super(AudioEvalMethodDNSMOS, self).__init__()
        self.eval_name = "dnsmos"
        self.dnsmos_uri = dnsmos_uri
        self.dnsmos_key = dnsmos_key
        self.required_sample_rate = ["16000"]
        self.required_channel = ["1"]

    def change_audio_config(self, audio_info : AudioInfo):
        if audio_info.sample_rate in self.required_sample_rate and audio_info.channel in self.required_channel:
            return None
        output = NamedTemporaryFile('w+t', suffix=".%s" % (audio_info.format_name))
        cmd = ["ffmpeg", "-i", audio_info.audio_path, "-ar", self.required_sample_rate[0], "-ac", self.required_channel[0], \
                "-vn", "-y", output.name]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8")

        return output

    def eval(self, dst_audio_info : AudioInfo):
        # Set the content type
        headers = {'Content-Type': 'application/json'}
        # If authentication is enabled, set the authorization header
        headers['Authorization'] = f'Basic {self.dnsmos_key}'
        
        fp_new_video = self.change_audio_config(dst_audio_info)
        dst_audio_info = AudioInfo(fp_new_video.name) if fp_new_video else dst_audio_info
        
        audio, fs = sf.read(dst_audio_info.audio_path)
        if fs != 16000:
            print('Only sampling rate of 16000 is supported as of now')
        data = {"data": audio.tolist()}
        input_data = json.dumps(data)
        # Make the request and display the response
        u = urlparse(self.dnsmos_uri)
        resp = requests.post(urljoin("https://" + u.netloc, 'score'), data=input_data, headers=headers)
        score_dict = resp.json()
        
        return score_dict["mos"]
    