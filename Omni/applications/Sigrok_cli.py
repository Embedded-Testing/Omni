import subprocess
import json
version = """sigrok-cli 0.7.2

Libraries and features:
- libsigrok 0.5.2/5:1:1 (rt: 0.5.2/5:1:1).
 - Libs:
  - glib 2.67.5 (rt: 2.72.4/7204:4)
  - libzip 1.7.3
  - libserialport 0.1.1/1:0:1 (rt: 0.1.1/1:0:1)
  - libusb-1.0 1.0.25.11696 API 0x01000108
  - hidapi 0.10.1
  - bluez 5.56
  - libftdi 1.5
  - Host: x86_64-pc-linux-gnu, little-endian.
  - SCPI backends: TCP, serial, USBTMC.
- libsigrokdecode 0.5.3/6:1:2 (rt: 0.5.3/6:1:2).
 - Libs:
  - glib 2.71.1 (rt: 2.72.4/7204:4)
  - Python 3.10.2 / 0x30a02f0 (API 1013, ABI 3)
  - Host: x86_64-pc-linux-gnu, little-endian."""


class SigrokCli:
    def __init__(self):
        pass

    def send_cmd(self, cmd) -> dict:
        cmd_dict = json.loads(cmd)
        payload = cmd_dict["payload"]
        command_list = ['sigrok-cli', payload]
        try:
            self.cmd_process = subprocess.Popen(
                command_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            cmd_dict["status"] = "done"
            return cmd_dict
        except Exception as e:
            exception_type = type(e).__name__
            error_msg = f'{exception_type}: {e}'
            cmd_dict["status"] = "error"
            cmd_dict["payload"] = error_msg
            return cmd_dict

    def get_response(self) -> dict:
        if self.cmd_process.poll() is None:
            return {"status": "busy", "payload": None}
        return {"status": "done", "payload": version}

    def get_cmd_status(self) -> dict:
        if (not hasattr(self, "cmd_process")):
            raise ValueError("No command sent. Call send_cmd first.")
        if self.cmd_process.poll() is None:
            return {"status": "busy"}
        else:
            return {"status": "done"}
