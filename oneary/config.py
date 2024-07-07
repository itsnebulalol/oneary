import json

from .utils import get_data_dir


class Config:
    def __init__(self):
        # Default configuration
        self.libraries = ["tv", "tv4k", "movies", "movies4k"]
        self.src_path = "/mnt/libraries"
        self.dest_path = "/mnt/library_organized"
        self.bind_address = "127.0.0.1"
        self.port = 5000

    def load(self):
        with open(get_data_dir() / "config.json", "r") as f:
            conf = json.load(f)
            self.__dict__.update(conf)

    def save(self):
        with open(get_data_dir() / "config.json", "w") as f:
            json.dump(self.__dict__, f, indent=4)
