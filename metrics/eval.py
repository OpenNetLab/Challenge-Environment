import os, sys, argparse, json, shutil

sys.path.append(os.getcwd())

from metrics.eval_audio import AudioEvaluation
from metrics.eval_video import VideoEvaluation


description = \
'''
Quickly Start:
python3 eval.py --src_video {src_video} --dst_video {dst_video} \
                --dst_audio {dst_audio} --dnsmos_uri {dnsmos_uri} --dnsmos_key {dnsmos_key} \
                --output {output json file}
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


def get_audio_score(args, eval_args):
    audio_eval_tool = AudioEvaluation(args.audio_eval_method, eval_args=eval_args)
    audio_out = audio_eval_tool.eval(args.dst_audio)
    return audio_out


def get_video_score(args, eval_args):
    video_eval_tool = VideoEvaluation(args.video_eval_method, eval_args=eval_args)
    video_out = video_eval_tool.eval(args.src_video, args.dst_video)
    return video_out


def init_tmp_dir():
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")
    os.mkdir("tmp")


def fill_args(args):
    ret = {}
    # for video
    if "video_size" in args:
        ret["video_size"] = args.video_size
    if "pixel_format" in args:
        ret["pixel_format"] = args.pixel_format
    if "bitdepth" in args:
        ret["bitdepth"] = args.bitdepth
    # for audio
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
        out_dict["audio"] = get_audio_score(args, eval_args)
        out_dict["video"] = get_video_score(args, eval_args)
    elif (args.method == "video"):
        out_dict["video"] = get_video_score(args, eval_args)
    elif (args.method == "audio"):
        out_dict["audio"] = get_audio_score(args, eval_args)

    print(out_dict)
    with open(args.output, 'w') as f:
        f.write(json.dumps(out_dict))
    