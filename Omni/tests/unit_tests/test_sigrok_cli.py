from Omni.applications.Sigrok_cli import SigrokCli
from Omni.tests.unit_tests.sigrok_responses.sigrok_resp import *
from unittest import mock
import pytest


@pytest.fixture
def mock_subprocess():
    with mock.patch('subprocess.Popen') as mock_subprocess:
        yield mock_subprocess


def test_sigrok_cli_sends_cmd(mock_subprocess):
    my_sigrok = SigrokCli()
    ret = my_sigrok.send_cmd("--version")
    mock_subprocess.assert_called_with(
        ["sigrok-cli", "--version"], shell=True, stdout=-1, stderr=-1, text=True)
    assert ret == {'status': 'done'}


@pytest.mark.parametrize("exception_type, exception_msg", [
    (Exception, "This is a dummy exception"),
    (ValueError, "This is a dummy exception2")
])
def test_sigrok_cli_sends_exception_on_error(mock_subprocess, exception_type, exception_msg):
    my_sigrok = SigrokCli()
    mock_subprocess.side_effect = exception_type(exception_msg)
    ret = my_sigrok.send_cmd("ERROR")
    assert ret == {'status': 'error',
                   'payload': f'{exception_type.__name__}: {exception_msg}'}


def test_sigrok_gets_response(mock_subprocess):
    mock_subprocess.return_value.poll.return_value = 0
    my_sigrok = SigrokCli()
    ret = my_sigrok.send_cmd("version")
    assert ret == {"status": "done"}
    rsp = my_sigrok.get_response()
    assert rsp['payload'] == version_rsp
    assert rsp['status'] == 'done'


def test_sigrok_gets_response_status_busy_if_cmd_not_finished(mock_subprocess):
    mock_subprocess.return_value.poll.return_value = None
    my_sigrok = SigrokCli()
    my_sigrok.send_cmd("version")
    rsp = my_sigrok.get_response()
    assert rsp == {"status": "busy", "payload": None}


def test_sigrok_get_cmd_status(mock_subprocess):
    mock_subprocess.return_value.poll.return_value = None
    my_sigrok = SigrokCli()
    my_sigrok.send_cmd("version")
    cmd_status = my_sigrok.get_cmd_status()
    assert cmd_status == {"status": "busy"}


def test_sigrok_get_cmd_status_without_cmd_raise_exception(mock_subprocess):
    mock_subprocess.return_value.poll.return_value = None
    my_sigrok = SigrokCli()
    with pytest.raises(ValueError, match="No command sent. Call send_cmd first."):
        cmd_status = my_sigrok.get_cmd_status()
