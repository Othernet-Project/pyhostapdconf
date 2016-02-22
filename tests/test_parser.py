try:
    from unittest import mock
except ImportError:
    import mock

import pytest

import hostapdconf.parser as mod


@pytest.mark.parametrize('line', ['# foo', '', '    ', '\n', '\t', '=foo'])
def test_parse_line_breaks(line):
    """ Comments, blanks, and malformed lines raise """
    with pytest.raises(mod.CommentOrBlankError):
        mod.HostapdConf.parse_line(line)


@pytest.mark.parametrize(
    'line,key,val',
    [('foo=bar', 'foo', 'bar'),
     ('foo =bar', 'foo', 'bar'),
     ('foo = bar', 'foo', 'bar'),
     ('foo= bar', 'foo', 'bar'),
     ('foo = bar baz', 'foo', 'bar baz'),
     ('foo= bar baz   ', 'foo', 'bar baz'),
     ('foo=bar\n', 'foo', 'bar'),
     ('foo=', 'foo', ''),
     ('foo=bar=baz', 'foo', 'bar=baz')]  # <-- Should we allow this case?
)
def test_parse_key_value(line, key, val):
    """ Key and values are parsed and stripped for whitespace """
    rkey, rval = mod.HostapdConf.parse_line(line)
    assert rkey == key
    assert rval == val


@mock.patch.object(mod.HostapdConf, 'reload')
def test_init_calls_reload(mock_reload):
    """ reload() method is called during instantiation """
    hc = mod.HostapdConf('foo')
    mock_reload.assert_called_once_with()


@mock.patch('hostapdconf.parser.open', new_callable=mock.mock_open)
def test_reload_opens_file(mock_open):
    """ When reload() is called, it opens the path specified in init """
    hc = mod.HostapdConf('foo')
    mock_open.assert_called_once_with('foo', 'r')


@mock.patch('hostapdconf.parser.open', new_callable=mock.mock_open)
def test_init_without_path(mock_open):
    """ When conf object is init'd w/o a path, reload quits early """
    hc = mod.HostapdConf()
    mock_open.assert_not_called()


def test_conf_loading_data(sample_conf_path):
    """ Parsed data is accessbile via internal data dict """
    hc = mod.HostapdConf(sample_conf_path)
    assert 'interface' in hc._data
    assert hc._data['interface'] == 'wlan0'


def test_conf_data_is_ordered(sample_conf_path):
    """ Parsed data should appear in file order """
    hc = mod.HostapdConf(sample_conf_path)
    first_few = list(hc._data.items())[:3]
    assert first_few == [
        ('interface', 'wlan0'),
        ('logger_syslog', '-1'),
        ('logger_syslog_level', '2')
    ]


def test_subscript_access(sample_conf_path):
    """ Parsed configuration is available as key """
    hc = mod.HostapdConf(sample_conf_path)
    assert hc['interface'] == 'wlan0'


def test_key_assignment(sample_conf_path):
    """ Parsed configuration can be assigned to using keys """
    hc = mod.HostapdConf(sample_conf_path)
    hc['interface'] = 'wlan1'
    assert hc._data['interface'] == 'wlan1'


def test_key_assignment_stringify():
    """ Assigned values are converted to strings """
    hc = mod.HostapdConf()
    hc['channel'] = 2
    assert hc['channel'] == '2'


def test_getting_keys(sample_conf_path):
    """ get() method can be used to get a key with fallback on default """
    hc = mod.HostapdConf(sample_conf_path)
    assert hc.get('interface', 'foo') == 'wlan0'
    assert hc.get('nonexistent', 'foo') == 'foo'
    assert hc.get('nonexistent') is None


def test_update(sample_conf_path):
    """ update() method can be used to update multiple keys """
    hc = mod.HostapdConf(sample_conf_path)
    hc.update({'foo': 'bar', 'bar': 'baz'})
    assert hc._data['foo'] == 'bar'
    assert hc._data['bar'] == 'baz'


def test_delete_key():
    """ Keys can be deleted using delete keyword """
    hc = mod.HostapdConf()
    hc['channel'] = 2
    del hc['channel']
    assert hc.get('channel') is None


def test_inclusion():
    """ Presence of a key can be tested with ``in`` keyword """
    hc = mod.HostapdConf()
    hc['channel'] = 2
    assert 'channel' in hc
    assert 'interface' not in hc


@pytest.mark.parametrize('dirty,clean', [
    ('foo\nbar', 'foo bar'),
    ('foo\n\rbar', 'foo bar'),
    ('foo\rbar', 'foo bar'),
    ('foo bar', 'foo bar'),
    ('foo ', 'foo'),
    ('\nfoo', 'foo'),
])
def test_clean_value(dirty, clean):
    """ Clean value strips out newlines and strips the string """
    assert mod.HostapdConf.clean_value(dirty) == clean


def test_serialize():
    """ serialize() converts the dict into a string """
    hc = mod.HostapdConf()
    hc['interface'] = 'wlan1'
    hc['ssid'] = 'Test'
    assert hc.serialize() == 'interface=wlan1\nssid=Test'


def test_write_without_path_fails():
    """ Calling write() without a path fails """
    hc = mod.HostapdConf()
    with pytest.raises(RuntimeError):
        hc.write()


def test_writes_to_file(temp_file):
    """ Calling write() persist the serialized config """
    hc = mod.HostapdConf(temp_file)
    hc['interface'] = 'wlan1'
    hc['ssid'] = 'Test'
    hc.write()
    with open(temp_file, 'r') as f:
        contents = f.read()
    assert 'interface=wlan1\nssid=Test' in contents


def test_passing_path_to_write(temp_file):
    """ Calling test with a path uses the specified path """
    hc = mod.HostapdConf()
    hc['interface'] = 'wlan2'
    hc['ssid'] = 'Test 1'
    hc.write(temp_file)
    with open(temp_file, 'r') as f:
        contents = f.read()
    assert 'interface=wlan2\nssid=Test 1' in contents


def test_write_header(temp_file):
    """ If optional header is specified, write() prepends it to config """
    hc = mod.HostapdConf()
    hc['ssid'] = 'Test'
    header = '# Auto-generated, do not edit.\n'
    hc.write(temp_file, header)
    with open(temp_file, 'r') as f:
        contents = f.read()
    assert contents == '# Auto-generated, do not edit.\nssid=Test'
