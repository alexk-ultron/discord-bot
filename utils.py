import datetime

import discum
from loguru import logger

import settings
from db.redis import redis
from services.telegram import TelegramService


def get_messages(bot: discum.Client, channel_id: str) -> list[dict]:
    max_num = 100
    last_msg_id = redis.get(channel_id)
    if not last_msg_id:
        total_messages = load_all_messages_after_date(
            bot=bot, channel_id=channel_id, max_num=max_num
        )
    else:
        total_messages = load_channel_messages_after_message(
            bot=bot, channel_id=channel_id, max_num=max_num, message_id=last_msg_id
        )

    # save last message id for redis for next run
    if total_messages:
        redis.set(key=channel_id, value=total_messages[0].get("id"))

    return total_messages[::-1]


def load_all_messages_after_date(bot: discum.Client, channel_id: str, max_num: int):
    total_messages = []
    messages = bot.getMessages(channelID=channel_id, num=max_num)
    messages_data = messages.json()
    (filtered_msgs, is_full_load) = filter_messages_by_date(
        messages_data, settings.date_from
    )
    total_messages.extend(filtered_msgs)

    while not is_full_load:
        messages = bot.getMessages(
            channelID=channel_id, beforeDate=total_messages[-1].get("id"), num=max_num
        )
        messages_data = messages.json()

        if not messages_data:
            break

        (filtered_msgs, is_full_load) = filter_messages_by_date(
            messages_data, settings.date_from
        )
        total_messages.extend(filtered_msgs)

    return total_messages


def load_channel_messages_after_message(
    bot: discum.Client, channel_id: str, max_num: int, message_id
):
    total_messages = []
    messages = bot.getMessages(
        channelID=channel_id, afterMessage=message_id, num=max_num
    )
    messages_data = messages.json()

    if len(messages_data) < max_num:
        return messages_data

    total_messages.extend(messages_data[::-1])

    while True:
        messages = bot.getMessages(
            channelID=channel_id, afterMessage=total_messages[-1].get("id"), num=max_num
        )
        messages_data = messages.json()

        total_messages.extend(messages_data[::-1])

        if len(messages_data) < max_num:
            break

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
    TelegramService.send_msg(log_msg)
