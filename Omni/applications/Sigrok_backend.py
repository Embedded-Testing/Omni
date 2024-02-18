import socket
import logging
import Omni.applications.Sigrok_cli as Sigrok_cli
import json

_bufsize = 4096

_error_msg_not_json = "Invalid test command. Received test command is not valid JSON."
_error_msg_bad_dict = "Invalid test command. Received test dictionary command does not contain type key."


def handle_omni_connection(client_connection):
    test_socket, client_address = client_connection
    logging.info(f"Connection established with {client_address}")
    data = test_socket.recv(_bufsize)
    command_str = data.decode('utf-8')
    logging.debug(f"Received test command: {command_str}")
    valid_cmd = __validade_cmd(command_str, test_socket)
    if (valid_cmd == True):
        cmd_instance = Sigrok_cli.SigrokCli()
        ret_dict = cmd_instance.send_cmd(command_str)
        test_socket.sendall(json.dumps(ret_dict).encode())
    data = test_socket.recv(_bufsize)
    command_str = data.decode('utf-8')
    logging.debug(f"Received test command: {command_str}")
    test_socket.close()


error_dict = {"type": "",
              "payload": "",
              "status": "error"
              }


def __validade_cmd(command_str, test_socket):
    try:
        command_dict = json.loads(command_str)
    except json.JSONDecodeError:
        error_msg = f"{_error_msg_not_json} Received: {command_str}"
        logging.error(error_msg)
        test_socket.sendall(error_msg.encode())
        return False
    if not 'type' in command_dict:
        error_msg = f"{_error_msg_bad_dict} Received: {command_str}"
        logging.error(error_msg)
        error_dict["payload"] = error_msg
        error_dict["status"] = "error"
        test_socket.sendall(json.dumps(error_dict).encode())
        return False
    return True


def sigrok_process(port, log_file_path):
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[logging.FileHandler(log_file_path),
                                  logging.StreamHandler()])
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', port))
    server_socket.listen(1)
    logging.info(f"Sigrok host application listening at {'localhost'}:{port}")
    logging.info("Waiting for connection...")
    client_connection = server_socket.accept()
    handle_omni_connection(client_connection)
    return
