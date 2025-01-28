import datetime

import discum
from loguru import logger


def get_messages_from_date(
    bot: discum.Client, channel_id: str, from_date: datetime
) -> list[dict]:
    total_messages = []
    max_num = 100
    messages = bot.getMessages(channelID=channel_id, num=max_num)
    messages_data = messages.json()
    (filtered_msgs, is_full_load) = filter_messages_by_date(messages_data, from_date)
    total_messages.extend(filtered_msgs)

    while not is_full_load:
        messages = bot.getMessages(
            channelID=channel_id, beforeDate=total_messages[-1].get("id"), num=max_num
        )
        messages_data = messages.json()

        if not messages_data:
            break

        (filtered_msgs, is_full_load) = filter_messages_by_date(
            messages_data, from_date
        )
        total_messages.extend(filtered_msgs)

    return total_messages[::-1]


def filter_messages_by_date(messages: list[dict], from_date: datetime):
    result = []
    is_full_load = False
    for msg in messages:
        if from_date <= datetime.datetime.fromisoformat(msg.get("timestamp")).replace(
            tzinfo=None
        ):
            result.append(msg)
        else:
            return result, True
    return result, is_full_load


def log_message(msg: dict, channel_data: dict):
    log_msg = f"{channel_data.get('name')} | {msg.get('content')} | https://discord.com/channels/{channel_data.get('guild_id')}/{msg.get('channel_id')}/{msg.get('id')}"
    logger.info(log_msg)
