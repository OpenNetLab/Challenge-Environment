import os, sys, argparse, json

sys.path.append(os.getcwd())

from metrics.eval_audio import AudioEvaluation


description = \
'''
Quickly Start:
python3 eval.py --src_video {src_video} --dst_video {dst_video}  --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key}
'''

def init_argparse():
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--method", type=str, default="simple", help="the method to evaluation")
    parser.add_argument("--output", type=str, default=None, help="the path of output file")
    # for video evaluation
    parser.add_argument("--video_eval_method", type=str, default="vmaf", help="the method to evaluate video, like vmaf")
    parser.add_argument("--src_video", type=str, default=None, help="the path of source video")
    parser.add_argument("--dst_video", type=str, default=None, help="the path of destination video")
    parser.add_argument("--frame_align", type=str, default="ffmpeg", help="how to do frame alignment")
    # required by the video format of yuv raw video
    parser.add_argument("--video_size", type=str, default=None, help="the size of video, like 1920x1080.Required by the video format of yuv")
    parser.add_argument("--pixel_format", type=str, default=None, help="pixel format (420/422/444)")
    parser.add_argument("--bitdepth", type=str, default=None, help="bitdepth (8/10/12)")

    # for audio evaluation
    parser.add_argument("--audio_eval_method", type=str, default="dnsmos", help="the method to evaluate audio, like DNSMOS")
    parser.add_argument("--dst_audio", type=str, default=None, help="the path of destination audio")
    parser.add_argument("--audio_sample_rate", type=str, default='16000', help="the sample rate of audio")
    parser.add_argument("--audio_channel", type=str, default='1', help="the numbers of audio channels")
    # for DNSMOS
    parser.add_argument("--dnsmos_uri", type=str, default=None, help="the uri to evaluate audio provided by DNSMOS")
    parser.add_argument("--dnsmos_key", type=str, default=None, help="the key to evaluate audio provided by DNSMOS")

    # for network evaluation
    parser.add_argument("--network_dir", type=str, default=None, help="the directory of network files")

    args = parser.parse_args()

    return args


def init_tmp_dir():
    if os.path.exists("tmp"):
        os.rmdir("tmp")
    os.mkdir("tmp")


def fill_args(args):
    ret = {}
    if "dnsmos_uri" in args:
        ret["dnsmos_uri"] = args.dnsmos_uri
    if "dnsmos_key" in args:
        ret["dnsmos_key"] = args.dnsmos_key
    if "audio_sample_rate" in args:
        ret["audio_sample_rate"] = args.audio_sample_rate
    if "audio_channel" in args:
        ret["audio_channel"] = args.audio_channel

    return ret


if __name__ == "__main__":
    
    args = init_argparse()
    eval_args = fill_args(args)
    init_tmp_dir()
    out_dict = {}
    if (args.method == "simple"):
        audio_eval_tool = AudioEvaluation(args.audio_eval_method, eval_args=eval_args)
        audio_out = audio_eval_tool.eval(args.dst_audio)

        out_dict["audio"] = audio_out
        
    print(out_dict)
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))
    