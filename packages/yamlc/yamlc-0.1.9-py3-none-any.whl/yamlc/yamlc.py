import yaml
import os
import sys
from threading import Lock

class Yamlc:
    _config = None
    _config_file = None
    _lock = Lock()
    
    @classmethod
    def _get_config_path(cls):
        """获取配置文件路径，按优先级顺序检查"""
        # 检查当前工作目录
        cwd_config = os.path.join(os.getcwd(), "config.yaml")
        if os.path.exists(cwd_config):
            return cwd_config
        
        # 获取主脚本目录并检查
        if getattr(sys, 'frozen', False):  # 处理打包情况
            main_script_dir = os.path.dirname(os.path.abspath(sys.executable))
        else:
            main_script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        main_config = os.path.join(main_script_dir, "config.yaml")
        return main_config


    @classmethod
    def _load_config(cls):
        with cls._lock:
            if cls._config is None:
                # print("加载配置文件...")
                if cls._config_file is None:
                    cls._config_file = cls._get_config_path()

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
            if not os.path.exists(path):
                raise FileNotFoundError(f"配置文件路径 {path} 不存在")
            cls._config_file = os.path.abspath(path)
        cls._load_config()