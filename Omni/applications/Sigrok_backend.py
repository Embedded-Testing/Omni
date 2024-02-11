import socket
import logging
import Omni.applications.Sigrok_cli as Sigrok_cli
import json

_bufsize = 4096

_error_msg_not_json = "Invalid test command. Received test command is not valid JSON."
_error_msg_bad_dict = "Invalid test command. Received test dictionary command does not contain command key."


def handle_omni_connection(client_connection):
    client_socket, client_address = client_connection
    logging.info(f"Connection established with {client_address}")
    data = client_socket.recv(_bufsize)
    command_str = data.decode('utf-8')
    logging.debug(f"Received test command: {command_str}")
    valid_cmd = __validade_cmd(command_str, client_socket)
    if (valid_cmd == True):
        cmd_instance = Sigrok_cli.SigrokCli()
        ret = cmd_instance.send_cmd(command_str)
        if (ret["status"] == "done"):
            client_socket.sendall("done".encode())
    # Hanlde command
    # Send command to sigrok-cli
    client_socket.close()


def __validade_cmd(command_str, client_socket):
    try:
        command_dict = json.loads(command_str)
    except json.JSONDecodeError:
        error_msg = f"{_error_msg_not_json} Received: {command_str}"
        logging.error(error_msg)
        client_socket.sendall(error_msg.encode())
        return False
    if not 'command' in command_dict:
        error_msg = f"{_error_msg_bad_dict} Received: {command_str}"
        logging.error(error_msg)
        client_socket.sendall(error_msg.encode())
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
