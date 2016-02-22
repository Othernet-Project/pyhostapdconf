try:
    from unittest import mock
except ImportError:
    import mock

import pytest


from hostapdconf.parser import HostapdConf
import hostapdconf.helpers as mod


def test_safe_del():
    """ _safe_del() can remove keys without raising on missing ones """
    d = {'foo': 'bar'}
    mod._safe_del(d, 'foo')
    try:
        mod._safe_del(d, 'foo')
    except Exception as e:
        pytest.fail('Expected no exception, got "%r"' % e)


def test_set_channel():
    """ set_channel() can be used to set channel key """
    hc = HostapdConf()
    mod.set_channel(hc, 2)
    assert hc['channel'] == '2'


def test_set_channel_out_of_bounds():
    """ Calling set_channel() with illegal channel raises """
    hc = HostapdConf()
    mod.set_channel(hc, 1)
    mod.set_channel(hc, 13)
    with pytest.raises(mod.ConfigurationError):
        mod.set_channel(hc, 14)
    with pytest.raises(mod.ConfigurationError):
        mod.set_channel(hc, 0)


def test_set_channel_for_north_america():
    """ For North America (US and Canada), max channel is 11 """
    hc = HostapdConf()
    mod.set_country(hc, 'US')
    mod.set_channel(hc, 1)
    mod.set_channel(hc, 11)
    with pytest.raises(mod.ConfigurationError):
        mod.set_channel(hc, 12)
    with pytest.raises(mod.ConfigurationError):
        mod.set_channel(hc, 13)
    with pytest.raises(mod.ConfigurationError):
        mod.set_channel(hc, 0)

