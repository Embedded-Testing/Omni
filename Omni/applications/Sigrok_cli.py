import subprocess
import json


class SigrokCli:
    def __init__(self):
        pass

    def send_cmd(self, cmd: str) -> dict:
        try:
            cmd_dict = json.loads(cmd)
            payload = cmd_dict["payload"]
            command_list = ['sigrok-cli', payload]
        except KeyError:
            error_msg = f'KeyError Invalid test command. Received test dictionary command does not contain type key. Received: {cmd}'
            return {"status": "error", "payload": error_msg}
        except json.JSONDecodeError:
            error_msg = f'''JSONDecodeError. Received test command is not a JSON-formatted string. Received: {cmd}.'''
            return {"status": "error", "payload": error_msg}
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
            return {"type": "get_response", "status": "busy", "payload": None}
        else:
            p_stdout, p_stderr = self.cmd_process.communicate()
            if self.cmd_process.returncode == 0:
                return {"type": "get_response", "status": "done", "payload": p_stdout}
            else:
                return {"type": "get_response", "status": "error", "payload": p_stderr}

    def get_cmd_status(self) -> dict:
        if (not hasattr(self, "cmd_process")):
            raise ValueError("No command sent. Call send_cmd first.")
        if self.cmd_process.poll() is None:
            return {"status": "busy"}
        else:
            return {"status": "done"}
