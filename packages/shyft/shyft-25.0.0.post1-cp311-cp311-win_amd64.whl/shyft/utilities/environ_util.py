from os import environ as environ
from ..time_series import win_crt_sync_environment_key


def set_environment(name: str, value: str):
    environ[name] = value
    win_crt_sync_environment_key(name)

