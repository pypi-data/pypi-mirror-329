"""Generate a status line for swaybar."""

import argparse
import logging
import tomllib
from pathlib import Path

from .config import Config
from .env import config_home, environ_path, environ_paths, self_name
from .io import start
from .logging import logger


def configure_logging(level: str) -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter("%(name)s: %(levelname)s: %(message)s"))
    logging.basicConfig(level=level.upper(), handlers=[stream_handler])


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=lambda prog: argparse.RawDescriptionHelpFormatter(
            prog, indent_increment=4, max_help_position=45
        ),
    )
    parser.add_argument(
        "-c",
        "--config-file",
        metavar="FILE",
        type=Path,
        help="override configuration file",
    )
    parser.add_argument(
        "-C",
        "--config-dir",
        metavar="DIRECTORY",
        type=Path,
        help="override configuration directory",
    )
    parser.add_argument(
        "-I",
        "--include",
        action="append",
        metavar="DIRECTORY",
        type=Path,
        help="include additional modules package",
    )
    parser.add_argument(
        "-i",
        "--interval",
        type=float,
        metavar="SECONDS",
        help="override default update interval",
    )
    parser.add_argument(
        "--click-events",
        dest="click_events",
        action="store_true",
        help="enable click events",
    )
    parser.add_argument(
        "--log-level",
        metavar="LEVEL",
        default="warning",
        choices=["debug", "info", "warning", "error", "critical"],
        help="override default minimum logging level (default: %(default)s)",
    )
    return parser.parse_args()


def load_config(args: argparse.Namespace) -> Config:
    config_dir: Path = args.config_dir or environ_path("SWAYSTATUS_CONFIG_DIR") or (config_home / self_name)
    config_file: Path = args.config_file or environ_path("SWAYSTATUS_CONFIG_FILE") or (config_dir / "config.toml")
    config = Config(**(tomllib.load(config_file.open("rb")) if config_file.is_file() else {}))
    config.include = (
        (args.include or [])
        + [config_dir / "modules"]
        + (config.include or [])
        + (environ_paths("SWAYSTATUS_PACKAGE_PATH") or [])
    )
    if args.interval:
        config.interval = args.interval
    if args.click_events:
        config.click_events = True
    return config


def main() -> int:
    args = parse_args()
    configure_logging(args.log_level)
    try:
        start(load_config(args))
    except Exception:
        logger.exception("Unhandled exception in main")
        return 1
    return 0
