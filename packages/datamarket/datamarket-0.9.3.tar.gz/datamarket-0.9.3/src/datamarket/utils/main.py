########################################################################################################################
# IMPORTS

import asyncio
import inspect
import logging
import random
import re
import shlex
import shutil
import subprocess
import time
from pathlib import Path
from typing import Literal, Union

import pendulum
from croniter import croniter
from configparser import RawConfigParser
from dynaconf import Dynaconf, add_converter

########################################################################################################################
# FUNCTIONS

logger = logging.getLogger(__name__)

Config = Union[RawConfigParser, Dynaconf]


def get_granular_date(
    granularity: Union[Literal["monthly", "biweekly", "weekly", "daily"], str], tz: str = "Europe/Madrid"
) -> pendulum.DateTime:
    """
    Returns the most recent date based on the given granularity or a custom cron expression.

    Args:
        granularity: Either a predefined value ("monthly", "biweekly", "weekly") or a custom cron expression.
        tz: Timezone to use for date calculations (default: "Europe/Madrid").

    Returns:
        A string representing the most recent date in the format "YYYY-MM-DD".

    Raises:
        ValueError: If the provided granularity or cron expression is invalid.
    """
    now = pendulum.now(tz)

    predefined_patterns = {
        "monthly": "0 0 1 * *",
        "biweekly": "0 0 1,15 * *",
        "weekly": "0 0 * * MON",
        "daily": "0 0 * * *",
        "now": "* * * * *",
    }

    cron_pattern = predefined_patterns.get(granularity, granularity)

    try:
        cron = croniter(cron_pattern, now)
        return cron.get_prev(pendulum.DateTime)
    except Exception as e:
        raise ValueError("Invalid cron expression or granularity specified.") from e


def read_converter(path_str: str):
    with open(path_str) as f:
        return f.read()


def get_config(
    config_file: Path, tz: str = "Europe/Madrid"
) -> Union[RawConfigParser, Dynaconf]:
    if Path(config_file).suffix == ".ini":
        logger.warning("Using legacy INI config reader. Please migrate to TOML")
        cfg = RawConfigParser()
        cfg.read(config_file)
        return cfg

    add_converter("read", read_converter)

    dt_now = get_granular_date("now", tz)
    dt_weekly = get_granular_date("weekly", tz)
    dt_biweekly = get_granular_date("biweekly", tz)

    config = Dynaconf(
        environments=True,
        env_switcher="SYSTYPE",
    )

    config.load_file(path=config_file)
    config.load_file(path=Path.home() / config_file.name)

    config.vars = {
        "year": dt_now.strftime("%Y"),
        "month": dt_now.strftime("%m"),
        "day": dt_now.strftime("%d"),
        "now": dt_now.strftime("%Y-%m-%d %H:%M:%S"),
        "now_stripped": dt_now.strftime("%Y%m%d%H%M%S"),
        "today": dt_now.strftime("%Y-%m-%d"),
        "today_stripped": dt_now.strftime("%Y%m%d"),
        "weekly_date": dt_weekly.strftime("%Y-%m-%d"),
        "weekly_date_stripped": dt_weekly.strftime("%Y%m%d"),
        "biweekly_date": dt_biweekly.strftime("%Y-%m-%d"),
        "biweekly_date_stripped": dt_biweekly.strftime("%Y%m%d"),
        "dynaconf_merge": True,
    }

    return config


def get_project_metadata():
    caller_frame = inspect.stack()[1]
    current_file_parts = Path(caller_frame.filename).resolve().parts
    src_index = current_file_parts.index("src")
    cmd_prefix = "dix vnc run --" if shutil.which("dix") else ""
    pkg_name = current_file_parts[src_index + 1]
    env_name = f"{pkg_name}_env"
    project_path = Path(*current_file_parts[:src_index])

    return {"cmd_prefix": cmd_prefix, "pkg_name": pkg_name, "env_name": env_name, "project_path": project_path}


def set_logger(level):
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(level.upper())
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    log.addHandler(ch)


def ban_sleep(max_time, min_time=0):
    sleep_time = int(random.uniform(min_time, max_time))  # noqa: S311
    logger.info(f"sleeping for {sleep_time} seconds...")
    time.sleep(sleep_time)


async def ban_sleep_async(max_time, min_time=0):
    sleep_time = int(random.uniform(min_time, max_time))  # noqa: S311
    logger.info(f"sleeping for {sleep_time} seconds...")
    await asyncio.sleep(sleep_time)


def run_bash_command(command):
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    text_lines = []
    for line_b in iter(p.stdout.readline, ""):
        line_str = line_b.decode().strip()

        if not line_str:
            break

        logger.info(line_str)
        text_lines.append(line_str)

    return "\n".join(text_lines)


def text_to_int(text):
    max_int32 = 2147483647
    parsed_str = re.sub(r"[^\d]", "", text)
    if parsed_str:
        num = int(parsed_str)
    else:
        return None

    if -max_int32 < num < max_int32:
        return num


def sleep_out_interval(from_h, to_h, tz="Europe/Madrid", seconds=1800):
    while pendulum.now(tz=tz).hour >= to_h or pendulum.now(tz=tz).hour < from_h:
        logger.warning("time to sleep and not scrape anything...")
        ban_sleep(seconds, seconds)


def sleep_in_interval(from_h, to_h, tz="Europe/Madrid", seconds=1800):
    while from_h <= pendulum.now(tz=tz).hour < to_h:
        logger.warning("time to sleep and not scrape anything...")
        ban_sleep(seconds, seconds)


def parse_field(dict_struct, field_path, format_method=None):
    if not isinstance(field_path, list):
        raise ValueError("Argument field_path must be of type list")

    field_value = dict_struct
    for field in field_path:
        if isinstance(field_value, dict):
            field_value = field_value.get(field)
        elif isinstance(field_value, list):
            field_value = field_value[field] if len(field_value) > field else None
        if field_value is None:
            return None
    return format_method(field_value) if format_method else field_value
