import psutil


def is_port_listening(port):
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            return True
    return False


def is_port_free(port):
    for conn in psutil.net_connections(kind='tcp'):
        if conn.laddr.port == port:
            return False
    return True


def get_process_listening_on_port(port):
    for conn in psutil.net_connections(kind='tcp'):
        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
            try:
                return psutil.Process(conn.pid)
            except psutil.NoSuchProcess:
                pass
