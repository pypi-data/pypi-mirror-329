import yaml
import os
import sys
from threading import Lock

class Yamlc:
    _config = None
    _config_file = os.path.join(os.getcwd(), "config.yaml")
    _lock = Lock()
    

    @classmethod
    def _load_config(cls):
        with cls._lock:
            if cls._config is None:
                if not os.path.exists(cls._config_file):
                    raise FileNotFoundError(f"{cls._config_file} not found")
                try:
                    with open(cls._config_file, 'r',encoding="utf-8") as f:
                        cls._config = yaml.safe_load(f) or {}
                except yaml.YAMLError as e:
                    raise ValueError(f"YAML 解析错误: {e}")

    @classmethod
    def get(cls, path, default=None):
        if cls._config is None:
            cls._load_config()  # 确保配置文件已加载
        keys = path.split('.')
        value = cls._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value

    @classmethod
    def reload(cls):
        with cls._lock:
            cls._config = None
            cls._load_config()

    @classmethod
    def load(cls, path: str = None) -> None:
        if cls._config is not None:
            return
        if path:
            cls._config_file = os.path.abspath(path)
        cls._load_config()