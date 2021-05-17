#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pytest, os


cur_dir = os.path.dirname(os.path.abspath(__file__))


def pytest_addoption(parser):
    parser.addoption("--dnsmos_uri", action="store")
    parser.addoption("--dnsmos_key", action="store")


@pytest.fixture
def dnsmos_uri(request):
    return request.config.getoption("--dnsmos_uri")


@pytest.fixture
def dnsmos_key(request):
    return request.config.getoption("--dnsmos_key")


@pytest.fixture(scope="module", params=[None, "None", "ffmpeg", "ocr"])
def align_method(request):
    return request.param


@pytest.fixture(scope="module", params=[cur_dir + "/data/test.y4m", cur_dir + "/data/test_labeled.y4m"])
def y4m_video(request):
    return request.param


@pytest.fixture(scope="module", params=[cur_dir + "/data/test.yuv"])
def yuv_video(request):
    return request.param