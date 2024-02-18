from Omni.applications.Sigrok_cli import SigrokCli
from .sigrok_data.sigrok_commands import measurement_command, malformed_dict_cmd, bad_cmd, help_command
from .sigrok_data.sigrok_resp import version_rsp, help_rsp
from unittest import mock
from unittest.mock import patch, MagicMock
import pytest
import json
import subprocess


@pytest.fixture
def mock_subprocess():
    with mock.patch('subprocess.Popen') as mock_subprocess:
        yield mock_subprocess


@pytest.fixture
def mock_communicate():
    mock_communicate = MagicMock()
    mock_communicate.returncode = 0
    yield mock_communicate


def test_sigrok_cli_sends_cmd(mock_subprocess):
    my_sigrok = SigrokCli()
    measurement_command_str = json.dumps(measurement_command)
    ret = my_sigrok.send_cmd(measurement_command_str)
    mock_subprocess.assert_called_with(
        ["sigrok-cli", "--version"], shell=True, stdout=-1, stderr=-1, text=True)
    assert ret == {'payload': '--version', 'type': 'command', 'status': 'done'}


def test_sigrok_cli_error_on_malformed_dict_cmd(mock_subprocess):
    my_sigrok = SigrokCli()
    command_str = json.dumps(malformed_dict_cmd)
    ret = my_sigrok.send_cmd(command_str)
    assert ret == {'status': 'error',
                   'payload': 'KeyError Invalid test command. Received test dictionary command does not contain type key. Received: {"bad_dict": "a malformed dict doesnt have a type key"}'}


def test_sigrok_cli_error_on_malformed_string_as_argument(mock_subprocess):
    my_sigrok = SigrokCli()
    ret = my_sigrok.send_cmd("not a JSON-formatted string")
    assert ret == {'status': 'error',
                   'payload': 'JSONDecodeError. Received test command is not a JSON-formatted string. Received: not a JSON-formatted string.'}


@pytest.mark.parametrize("sigrok_cmd, send_payload", [
    (json.dumps(measurement_command), '--version'),
    (json.dumps(help_command), '--help'),
])
def test_sigrok_gets_response(mock_subprocess, mock_communicate, sigrok_cmd, send_payload):
    mock_subprocess.return_value.poll.return_value = 0
    mock_communicate.communicate.return_value = (version_rsp, b'')
    mock_subprocess.return_value = mock_communicate
    my_sigrok = SigrokCli()
    ret = my_sigrok.send_cmd(sigrok_cmd)
    assert ret == {'payload': send_payload,
                   'type': 'command', 'status': 'done'}
    rsp = my_sigrok.get_response()
    assert rsp['type'] == 'get_response'
    assert rsp['payload'] == version_rsp
    assert rsp['status'] == 'done'


def test_sigrok_gets_response_status_busy_if_cmd_not_finished(mock_subprocess):
    mock_subprocess.return_value.poll.return_value = None
    my_sigrok = SigrokCli()
    measurement_command_str = json.dumps(measurement_command)
    my_sigrok.send_cmd(measurement_command_str)
    rsp = my_sigrok.get_response()
    assert rsp == {"type": "get_response", "status": "busy", "payload": None}


def test_sigrok_get_cmd_status_without_cmd_raise_exception(mock_subprocess):
    my_sigrok = SigrokCli()
    with pytest.raises(ValueError, match="No command sent. Call send_cmd first."):
        cmd_status = my_sigrok.get_cmd_status()
