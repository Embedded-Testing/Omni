import pytest
from unittest.mock import MagicMock, patch
from Omni.applications.Sigrok_backend import sigrok_process
from Omni.applications.Sigrok import launch_sigrok_process_host, verify_sigrok_process
from Omni.process_manager.process_manager import create_config_file
from Omni.process_manager.exceptions import ProcessStartupError, PortBusyError
import os
import pathlib
import shutil
import psutil
import pytest

temporary_folder = pathlib.Path("./TempSigrok")
log_file_path = temporary_folder / "SigrokLog.txt"
default_port = 10430


@pytest.fixture(scope="session", autouse=True)
def create_temp_folder():
    folder_name = temporary_folder
    folder_name.mkdir(parents=True, exist_ok=True)
    yield


@pytest.fixture(scope="session", autouse=True)
def cleanup_temp_folder():
    yield
    if os.path.exists(temporary_folder):
        shutil.rmtree(temporary_folder)


@pytest.fixture
def mock_sigrok_process(mocker):
    mock = mocker.patch(
        'Omni.applications.Sigrok.multiprocessing.Process', spec=True)
    mock.return_value = MagicMock()
    mock.return_value.pid = 1234
    return mock


@pytest.fixture
def create_dummy_process_file():
    process_file_path = temporary_folder / "DummyProcess.json"
    create_config_file(process_file_path)
    yield process_file_path
    os.remove(process_file_path)


@pytest.fixture
def create_bad_format_process_file():
    bad_format_process_file_path = temporary_folder / "my_bad_format_file.json"
    with open(bad_format_process_file_path, 'w') as f:
        f.write('This is a dummy file.')
    yield bad_format_process_file_path
    os.remove(bad_format_process_file_path)


@pytest.fixture
def mock_os_exit(mocker):
    return mocker.patch('os._exit')


@pytest.fixture
def mock_append_process_data_to_file(mocker):
    mock = mocker.patch(
        'Omni.process_manager.process_manager.append_process_data_to_file', side_effect=None)
    return mock


@pytest.fixture
def mock_net_connections_busy(mocker):
    mock_net_connections = [MagicMock()]
    mock_net_connections[0].status = psutil.CONN_LISTEN
    mock_net_connections[0].laddr.port = default_port
    mock = mocker.patch('psutil.net_connections',
                        return_value=mock_net_connections)
    return mock


@pytest.fixture
def mock_net_connections_none(mocker):
    mock_net_connections = [MagicMock()]
    mock = mocker.patch('psutil.net_connections',
                        return_value=mock_net_connections)
    return mock


@pytest.fixture
def mock_net_connections_standard(mocker):
    mock_net_connections_none = [MagicMock()]
    mock_net_connections_busy = [MagicMock()]
    mock_net_connections_busy[0].status = psutil.CONN_LISTEN
    mock_net_connections_busy[0].laddr.port = default_port
    mock = mocker.patch('psutil.net_connections',
                        side_effect=[mock_net_connections_none, mock_net_connections_busy])
    return mock


def test_launch_sigrok_process_host_correct_call(mock_sigrok_process, mock_net_connections_standard, mock_os_exit, create_dummy_process_file):
    dummy_process_file_path = create_dummy_process_file
    port = 10430
    launch_sigrok_process_host(port, dummy_process_file_path, log_file_path)
    mock_sigrok_process.assert_called_once_with(
        target=sigrok_process, args=(port, log_file_path))
    mock_sigrok_process.return_value.start.assert_called_once()
    mock_os_exit.assert_called_once_with(0)


def test_launch_sigrok_process_host_raises_exception_if_process_file_dont_exist(mock_sigrok_process, mock_os_exit):
    port = default_port
    with pytest.raises(FileNotFoundError):
        launch_sigrok_process_host(
            default_port, 'non_existing_file.txt', log_file_path)


def test_launch_sigrok_process_host_do_not_raises_if_process_file_exist(mock_sigrok_process, mock_net_connections_standard, mock_os_exit, create_dummy_process_file):
    launch_sigrok_process_host(
        default_port, create_dummy_process_file, log_file_path)


def test_launch_sigrok_process_host_raises_exception_if_file_has_bad_format(mock_sigrok_process, mock_os_exit, create_bad_format_process_file):
    bad_format_process_file_path = create_bad_format_process_file
    with pytest.raises(ValueError):
        launch_sigrok_process_host(
            default_port, bad_format_process_file_path, log_file_path)


def test_launch_sigrok_append_sigrok_entry_to_log(mock_sigrok_process, mock_os_exit, mock_net_connections_standard, create_dummy_process_file, mock_append_process_data_to_file):
    dummy_process_file_path = create_dummy_process_file
    launch_sigrok_process_host(
        default_port, dummy_process_file_path, log_file_path)
    sigrok_append_process_data_args = mock_append_process_data_to_file.call_args[0][0]
    print(sigrok_append_process_data_args)
    assert (sigrok_append_process_data_args["application"] == "Sigrok process")
    assert (sigrok_append_process_data_args["pid"]
            == mock_sigrok_process.return_value.pid)
    assert (
        sigrok_append_process_data_args["log_file"] == str(log_file_path))
    assert (
        sigrok_append_process_data_args["process_call"] == "multiprocessing in launch_sigrok_process_host in Sigrok_process.py")
    assert (sigrok_append_process_data_args["port"] == default_port)
    assert (
        sigrok_append_process_data_args["pgrep_string"] == "Sigrok_process")


def test_verify_sigrok_process_no_exception_if_process_is_running(mock_sigrok_process, mock_os_exit, create_dummy_process_file, mock_net_connections_standard):
    launch_sigrok_process_host(
        default_port, create_dummy_process_file, log_file_path)
    verify_sigrok_process(default_port)


def test_verify_sigrok_raise_exception_if_process_not_running(mock_sigrok_process, mock_os_exit, create_dummy_process_file, mock_net_connections_none):
    launch_sigrok_process_host(
        default_port, create_dummy_process_file, log_file_path)
    with pytest.raises(ProcessStartupError):
        verify_sigrok_process(default_port)


@pytest.mark.parametrize("process_id", [1234, 5678])
def test_verify_sigrok_raise_exception_if_port_busy(mock_sigrok_process, mock_os_exit, create_dummy_process_file, mock_net_connections_busy, mocker, process_id):
    mocker.patch('psutil.Process', return_value=process_id)
    with pytest.raises(PortBusyError, match=f"Port {default_port} is in use by process with id {process_id}"):
        launch_sigrok_process_host(
            default_port, create_dummy_process_file, log_file_path)
