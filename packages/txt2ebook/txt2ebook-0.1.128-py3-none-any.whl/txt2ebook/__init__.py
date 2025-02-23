# Copyright (c) 2021,2022,2023,2024,2025 Kian-Meng Ang
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Common shared functions."""

import argparse
import logging
import platform
import sys

import langdetect

logger = logging.getLogger(__name__)

__version__ = "0.1.126"


def setup_logger(config: argparse.Namespace) -> None:
    """Sets up logging configuration based on command-line arguments.

    Args:
        config (argparse.Namespace): Namespace containing parsed arguments.
    """
    if config.quiet:
        logging.disable(logging.NOTSET)
        return

    level = logging.DEBUG if config.debug else logging.INFO
    format_string = (
        "%(levelname)5s: %(message)s" if config.debug else "%(message)s"
    )

    logging.basicConfig(
        level=level,
        format=format_string,
        stream=sys.stdout,
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def log_or_raise_on_warning(msg: str, raise_on_warning: bool = False) -> None:
    """Log warnings or raise it as exception.

    Args:
        msg(str): Warning message.
        raise_on_warning(bool): To raise exception instead of logging.
    """
    if raise_on_warning:
        raise RuntimeError(msg)

    logger.warning(msg)


def print_env() -> None:
    """Print environment details for bug reporting."""
    sys_version = sys.version.replace("\n", "")
    print(
        f"txt2ebook: {__version__}",
        f"python: {sys_version}",
        f"platform: {platform.platform()}",
        sep="\n",
    )


def detect_and_expect_language(content: str, config_language: str) -> str:
    """Detect and expect the language of the txt content."""
    detect_language = langdetect.detect(content)
    config_language = config_language or detect_language
    logger.info("Config language: %s", config_language)
    logger.info("Detect language: %s", detect_language)

    if config_language and config_language != detect_language:
        logger.warning(
            "Config (%s) and detect (%s) language mismatch",
            config_language,
            detect_language,
        )
    return config_language
