from .base import BaseConfig


class EnvConfig(BaseConfig):
    def __init__(self, dir="config/"):
        super().__init__("env", dir)

    def _load_file(self, file_path):
        config = {}
        with open(file_path, "r") as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
