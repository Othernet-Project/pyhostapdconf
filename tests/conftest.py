import pytest

import os
import time
import shutil
from os.path import dirname, join

TESTDIR = dirname(__file__)
SAMPLE_CONF = join(dirname(dirname(__file__)), 'example/hostapd_example.conf')
TEST_CONF = join(TESTDIR, 'hostapd.conf')


@pytest.yield_fixture
def sample_conf_path():
    """ Return the path to sample configuration file """
    shutil.copyfile(SAMPLE_CONF, TEST_CONF)
    yield TEST_CONF
    os.unlink(TEST_CONF)


@pytest.yield_fixture
def temp_file():
    """ Return a temporary file """
    tf = join(TESTDIR, 'tmp-{}.conf'.format(int(time.time() * 10000)))
    with open(tf, 'a'):
        os.utime(tf, None)  # second arg required under py2
    yield tf
    os.unlink(tf)
