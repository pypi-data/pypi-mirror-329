from pathlib import Path
from yaml import load

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader


class Config:

    def __init__(self, config_path: Path):
        with open(config_path, "r", encoding="utf-8") as file:
            self.yaml_config = load(file.read(), Loader=Loader)

    def get(self, key):
        return self.yaml_config[key]
