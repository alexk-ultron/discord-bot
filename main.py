import datetime
import random
import re
import time

import discum
from loguru import logger

import settings
from db.redis import redis
from utils import log_message, get_messages

bot = discum.Client(email=settings.email, password=settings.password, log=False)


@bot.gateway.command  # indicates a function as an event, in this case a gateway event
def on_ready(resp):
    if resp.event.ready_supplemental:
        user = bot.gateway.session.user  # parsing the current user
        logger.info(f'Logged in as {user.get("username")}')
        logger.info(f"Start parsing messages from {settings.date_from}")

        random.shuffle(settings.channels)

        for channel_id in settings.channels:

            channel = bot.getChannel(channelID=channel_id)
            # check if channel exist
            if channel.status_code != 200:
                logger.error(f"Channel with id={channel_id} not found")
                continue

            channel_data = channel.json()

            messages_data = get_messages(bot=bot, channel_id=channel_id)

            if messages_data:
                for msg in messages_data:
                    if re.findall(settings.keywords_pattern, msg.get("content")):
                        log_message(msg, channel_data)

            time.sleep(random.uniform(*settings.sleep_delay_range))

        bot.gateway.resetSession()
        bot.gateway.close()


redis.init()
bot.gateway.run(auto_reconnect=True)
redis.close()
