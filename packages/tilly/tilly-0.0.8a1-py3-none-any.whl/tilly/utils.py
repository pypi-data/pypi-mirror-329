import os
import json
import pathlib

import click

def static_folder():
    config = load_config(local_config=True)
    return config.get("TILLY_OUTPUT_FOLDER", "_static")

def get_app_dir():
    path = pathlib.Path(click.get_app_dir("tilly"))
    path.mkdir(exist_ok=True, parents=True)
    return path

def load_config(global_config=None, local_config=None):
    if global_config:
        return json.loads(global_config_file().read_text()) if global_config_file().exists() else {}

    if local_config:
        return json.loads(local_config_file().read_text()) if local_config_file().exists() else {}

def add_config_to_env():
    """Add config to environment."""
    config = load_config(local_config=True)
    os.environ = {**os.environ, **config}

def global_config_file():
    return get_app_dir() / "config.json"

def local_config_file():
    root = pathlib.Path.cwd()
    return root / "config.json"
