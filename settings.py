import datetime
import os
import re

from dotenv import load_dotenv
from loguru import logger

load_dotenv()

date_time_now = datetime.datetime.utcnow()

file_log_format = "{time:YYYY-MM-DD HH:mm} | <b>{message}</b>"
logger.add(
    f"logs/file-{date_time_now}",
    format=file_log_format,
    colorize=False,
    backtrace=True,
    diagnose=True,
)

email = os.environ.get("EMAIL")
password = os.environ.get("PASSWORD")

# Sleep delay in seconds
sleep_delay_range = [1, 2]

# timeframe between messages from the current time for loading in hours
messages_timeframe = 30

# TODO: list with channels id for scan https://docs.statbot.net/docs/faq/general/how-find-id/
channels = [
    "1332010133919895632",
    "1332000594948263936",
    "1332000594948263911",
]

# TODO: list with keywords
keywords = ["2", "test"]

keywords_pattern = "|".join(re.escape(k) for k in keywords)  # Whole words only
