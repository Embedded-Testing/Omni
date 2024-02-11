import pytest
from Omni.applications.Sigrok_backend import *
import pathlib
import shutil
import os
import pytest
from unittest.mock import MagicMock
import json


@pytest.fixture
def socket_mock(mocker):
    server_socket_mock = mocker.patch(
        'Omni.applications.Sigrok_backend.socket.socket')
    mock_connected_socket = mocker.MagicMock()
    mock_address = ('client_host', 12345)
    server_socket_mock.return_value.accept.return_value = (
        mock_connected_socket, mock_address)
    yield server_socket_mock, mock_connected_socket


@pytest.fixture
def sigrok_cli_mocker(mocker):
    MockSigrokCli = mocker.patch(
        'Omni.applications.Sigrok_backend.Sigrok_cli.SigrokCli')
    mock_send_cmd = MagicMock()
    MockSigrokCli.return_value.send_cmd = mock_send_cmd
    yield MockSigrokCli, mock_send_cmd


@pytest.fixture
def logging_mock(mocker):
    log_mock = mocker.patch('Omni.applications.Sigrok_backend.logging')
    yield log_mock


temporary_folder = pathlib.Path("./TempSigrok")
log_file_path = os.path.abspath(temporary_folder / "SigrokLog.txt")


@pytest.fixture(scope="session", autouse=True)
def create_temp_folder():
    folder_name = temporary_folder
    folder_name.mkdir(parents=True, exist_ok=True)
    yield
    if os.path.exists(temporary_folder):
        shutil.rmtree(temporary_folder)


def test_sigrok_backend_binds_socket(socket_mock):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = json.dumps(command_dict)
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    server_socket.return_value.bind.assert_called_once_with(
        ('localhost', 1234))
    server_socket.return_value.listen.assert_called_once_with(
        1)
    server_socket.return_value.accept.assert_called_once()


def test_sigrok_backend_logs_bind_msgs(socket_mock, logging_mock):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = json.dumps(command_dict)
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    logging_mock.info.assert_any_call(
        'Sigrok host application listening at localhost:1234')
    logging_mock.info.assert_any_call(
        'Waiting for connection...')


def test_sigrok_backend_waits_for_data(socket_mock):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = json.dumps(command_dict)
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    client_socket.recv.assert_called_once_with(4096)


command_dict = {
    "command": "Sigrok dummy cmd",
}

command_dict2 = {
    "command": "--version",
}

bad_dict_cmd = {
    "bad_dict": "a bad string",
}


@pytest.mark.parametrize("dummy_cmd_dict", [command_dict, command_dict2])
def test_sigrok_backend_recv_data(socket_mock, logging_mock, dummy_cmd_dict):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = json.dumps(dummy_cmd_dict)
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    logging_mock.debug.assert_called_with(
        f'Received test command: {dummy_cmd__str}')


def test_sigrok_backend_recv_data_logs_error_on_non_json_cmd(socket_mock, logging_mock):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = "This is not a JSON string."
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    logging_mock.error.assert_called_with(
        f"Invalid test command. Received test command is not valid JSON. Received: {dummy_cmd__str}")
    client_socket.sendall.assert_called_with(
        f"Invalid test command. Received test command is not valid JSON. Received: {dummy_cmd__str}".encode())


def test_sigrok_backend_recv_data_logs_error_on_malformed_cmd_dict(socket_mock, logging_mock):
    server_socket, client_socket = socket_mock
    dummy_cmd__str = json.dumps(bad_dict_cmd)
    client_socket.recv.return_value = dummy_cmd__str.encode()
    sigrok_process(1234, log_file_path)
    logging_mock.error.assert_called_with(
        f"Invalid test command. Received test dictionary command does not contain command key. Received: {dummy_cmd__str}")
    client_socket.sendall.assert_called_with(
        f"Invalid test command. Received test dictionary command does not contain command key. Received: {dummy_cmd__str}".encode())


def test_sigrok_backend_sends_cmd_to_cli(socket_mock, logging_mock, sigrok_cli_mocker):
    server_socket, client_socket = socket_mock
    sigrok_cli_mock, mock_send_cmd = sigrok_cli_mocker
    dummy_cmd_str = json.dumps(command_dict)
    client_socket.recv.return_value = dummy_cmd_str.encode()
    sigrok_process(1234, log_file_path)
    mock_send_cmd.assert_called_with(dummy_cmd_str)


def test_sigrok_backend_answers_done_if_cmd_done(socket_mock, logging_mock, sigrok_cli_mocker):
    server_socket, client_socket = socket_mock
    sigrok_cli_mock, mock_send_cmd = sigrok_cli_mocker
    mock_send_cmd.return_value = {"status": "done"}
    dummy_cmd_str = json.dumps(command_dict)
    client_socket.recv.return_value = dummy_cmd_str.encode()
    sigrok_process(1234, log_file_path)
    client_socket.sendall.assert_called_with("done".encode())
    mock_send_cmd.assert_called_with(dummy_cmd_str)
