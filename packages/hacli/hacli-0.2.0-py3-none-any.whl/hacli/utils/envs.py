import os

import typer
import yaml


def convert_to_env_vars(d, prefix=""):
    env_vars = {}

    for key, value in d.items():
        if isinstance(value, dict):
            env_vars.update(convert_to_env_vars(value, prefix + key.upper() + "_"))
        else:
            env_vars[prefix + key.upper()] = value

    return env_vars


def load_yaml_env_vars():
    home_dir = os.path.expanduser("~")
    yml_file_path = os.path.join(home_dir, ".config", "hacli", "setting.yaml")

    if os.path.exists(yml_file_path):
        with open(yml_file_path, 'r') as file:
            config = yaml.safe_load(file)
            env_vars = convert_to_env_vars(config)
            for key, value in env_vars.items():
                os.environ[key] = value
                print(key, value)
    else:
        print(f"File {yml_file_path} does not exist.")
        raise typer.Exit(1)
