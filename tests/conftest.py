import pytest


def pytest_addoption(parser):
    parser.addoption("--dnsmos_uri", action="store")
    parser.addoption("--dnsmos_key", action="store")


@pytest.fixture
def dnsmos_uri(request):
    return request.config.getoption("--dnsmos_uri")


@pytest.fixture
def dnsmos_key(request):
    return request.config.getoption("--dnsmos_key")