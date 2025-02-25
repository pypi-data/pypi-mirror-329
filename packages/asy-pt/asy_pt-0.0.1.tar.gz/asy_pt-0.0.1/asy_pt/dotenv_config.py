# -*- coding: utf-8 -*-
# @Time    : 2025/2/19 15:36
# @Author  : xuwei
# @FileName: dotenv_config.py
# @Software: PyCharm


from dotenv import load_dotenv
import os

_env_loaded = False

_config_file = os.getenv("CONFIG_FILE", default=None)
print("dotenv_path: ", _config_file)


def load_env_once():
    global _env_loaded
    if not _env_loaded:
        load_dotenv(dotenv_path=_config_file)
        _env_loaded = True


# 只会加载一次
load_env_once()


def config(label: str, key: str, default=None):
    # label是.evn中的前缀，类似于APP_xxx
    return os.getenv(label.upper() + "_" + key.upper(), default=default)
