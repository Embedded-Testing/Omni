import json
import os
import subprocess


class InvalidProcessEntry(Exception):
    pass


def check_file_exists(file_path):
    return os.path.isfile(file_path)


def _error_msg_file_already_exists(filename):
    print("##################################################")
    print("#########   ERROR: FILE ALREADY EXISTS   #########")
    print("##################################################")
    print(f"Error: File '{filename}' already exists!")


def create_config_file(filename):
    if (check_file_exists(filename) == True):
        _error_msg_file_already_exists(filename)
    else:
        _create_empty_process_file(filename)


def delete_config_file(file_path):
    if (load_processes(file_path) == []):
        os.remove(file_path)
    return


def _create_empty_process_file(filename):
    with open(filename, "w") as json_file:
        json.dump([], json_file)


def _verify_valid_process_data(my_dict):
    minimal_keys_list = ["application", "pid", "pgrep_string", "process_call"]
    if (all(key in my_dict for key in minimal_keys_list) == False):
        raise InvalidProcessEntry(
            'Missing keys in process dictionary. Minimal expected Keys: '+str(minimal_keys_list))


def append_process_data_to_file(data, config_file):
    _verify_valid_process_data(data)
    json_data = load_processes(config_file)
    json_data.append(data)
    save_processes(config_file, json_data)


def save_processes(config_file, json_data):
    with open(config_file, "w") as file:
        json.dump(json_data, file, indent=4)


def load_processes(config_file):
    with open(config_file, "r") as file:
        json_data = json.load(file)
    return json_data


def pretty_print_json(data):
    print(json.dumps(data, indent=4))


def close_applications(config_file):
    verify_file(config_file)
    json_data = load_processes(config_file)
    for application in json_data:
        pid = application["pid"]
        kill_command = ["kill", pid]
        print(kill_command)
        subprocess.run(kill_command)


def verify_file(process_file):
    __verify_file_exists(process_file)
    __verify_file_format(process_file)


def __verify_file_exists(process_file):
    if (os.path.isfile(process_file) == False):
        raise FileNotFoundError(f"file '{process_file}' not found")


def __verify_file_format(process_file):
    with open(process_file, "r") as file:
        json_data = json.load(file)
        if (type(json_data) != list):
            raise ValueError(
                f"file '{process_file}' has bad format expected list")
