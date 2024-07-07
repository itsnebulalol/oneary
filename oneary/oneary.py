from argparse import Namespace
from pathlib import Path
from shutil import copy
from sys import exit

from . import utils, logger
from .config import Config
from .logger import colors
from .webhooks import WebhookApp


class Oneary:
    def __init__(self, args: Namespace) -> None:
        self.args = args

        self.data_dir = None
        self.config = None
        self.src_path = None
        self.dest_path = None

    def main(self) -> None:
        """Main function"""

        print(
            colors["bold"]
            + colors["lightblue"]
            + "Oneary"
            + colors["reset"]
            + colors["bold"]
            # + f" | version {utils.get_version()}"
            + colors["reset"]
        )
        print("Made with \u2764 by Nebula")

        self.data_dir = utils.get_data_dir()
        self.data_dir.mkdir(exist_ok=True, parents=True)
        logger.debug(f'Data directory is "{self.data_dir}"', self.args.debug)

        self.config = Config()
        if Path(self.data_dir / "config.json").exists():
            self.config.load()
        else:
            logger.debug("Creating configuration file", self.args.debug)
            self.config.save()
        logger.debug(self.config.__dict__, self.args.debug)

        logger.log("Checking paths")
        if Path(self.config.src_path).exists() or Path(self.config.dest_path).exists():
            self.src_path = Path(self.config.src_path)
            self.dest_path = Path(self.config.dest_path)
        else:
            logger.error("Source and/or destination paths do not exist")
            exit(1)

        logger.log("Starting initial scan")
        self.process()

        logger.log("Setting up webhook server")
        print(
            f"Starting webhook server on port {self.config.port} ({self.config.bind_address})"
        )
        webhook = WebhookApp(self.config)
        webhook.add_endpoint(
            endpoint="/process",
            endpoint_name="process",
            handler=self.process,
            methods=["POST"],
        )
        webhook.run()

    def process(self) -> None:
        """Actual copy process"""

        print("Searching files")
        utils.erase_dir(self.dest_path / "movies")
        utils.erase_dir(self.dest_path / "tv")

        for library in self.config.libraries:
            src_library = Path(self.src_path / library)
            if not src_library.exists():
                logger.error(f'Library "{library}" does not exist')
                exit(1)

            for f in src_library.glob("**/*"):
                if f.is_file() and not f.name in (".DS_Store", "Thumbs.db"):
                    path = str(f).split("/")

                    if library.startswith("tv"):
                        name = path[-3]
                        season = path[-2]
                        episode = path[-1]
                        print(f"Linking {library}/{name}/{season}/{episode}")

                        dest_series = Path(self.dest_path / "tv" / name / season)
                        dest_series.mkdir(exist_ok=True, parents=True)
                        copy(f, dest_series, follow_symlinks=False)
                    elif library.startswith("movies"):
                        name = path[-2]
                        movie = path[-1]
                        print(f"Linking {library}/{name}/{movie}")

                        dest_movie = Path(self.dest_path / "movies" / name)
                        dest_movie.mkdir(exist_ok=True, parents=True)
                        copy(f, dest_movie, follow_symlinks=False)
