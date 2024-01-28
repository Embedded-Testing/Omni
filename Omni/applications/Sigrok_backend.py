import socket
import logging
import Omni.applications.Sigrok_cli as Sigrok_cli

_bufsize = 4096


def handle_omni_connection(client_socket, client_address):
    logging.info(f"Connection established with {client_address}")
    data = client_socket.recv(_bufsize)
    data_string = data.decode('utf-8')
    logging.debug(f"Received command: {data_string}")
    cmd_instance = Sigrok_cli.SigrokCli()
    ret = cmd_instance.send_cmd(data_string)
    if (ret["status"] == "done"):
        client_socket.sendall("done".encode())
    # Hanlde command
    # Send command to sigrok-cli
    client_socket.close()


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
    client_socket, address = server_socket.accept()
    handle_omni_connection(client_socket, address)
    return
