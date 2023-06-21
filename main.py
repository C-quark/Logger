from telethon import TelegramClient, events
from datetime import datetime
import os
import logging
import db
from config import api_id, api_hash, SAVE, CHAT


logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", format="%(asctime)s %(levelname)s %(message)s")


client = TelegramClient('session', api_id, api_hash, device_model='Redmi Note 12 Pro', system_version='14.0.9', app_version='10.3.1', lang_code='en', system_lang_code='en-US')
client.start()
now = datetime.now()

database_name = 'logger.db'
database = db.Database(database_name)


def update_users(users):
    for user in users:
        if user.first_name is not None:
            database.update_username(user.first_name, user.id)


@client.on(events.MessageEdited)
async def handler(event):
    if event.chat_id != CHAT:
        return

    date = now.date()
    time = now.strftime('%I:%M:%S')
    sender_id = event.sender_id
    edit_message_tg = event.message
    edit_message_sql = event.message.message
    tg_id = event.id
    edit = 'Edit'

    await client.forward_messages(SAVE, edit_message_tg)

    database.edit(date, time, sender_id, tg_id, edit_message_sql, edit)
    users = await client.get_participants(CHAT)
    update_users(users)
    database.commit()


@client.on(events.MessageDeleted)
async def handler(event):
    if event.chat_id != CHAT:
        return

    date = now.date()
    time = now.strftime('%I:%M:%S')
    delete = 'Delete'

    for tg_id in event.deleted_ids:
        database.delete(date, time, delete, tg_id)
        database.commit()


@client.on(events.NewMessage)
async def event_handler(event):
    #print(event.chat_id, event.sender_id, event.raw_text)

    if event.chat_id != CHAT:
        return

    reply_message = []
    sender_id = event.sender_id
    message_text = event.raw_text
    message = event.message
    tg_id = event.id
    reply_mes_id = None
    date = now.date()
    time = now.strftime('%I:%M:%S')

    if message.media is not None:
        if not os.path.isdir("logger_files"):
            os.mkdir("logger_files")
        path = f"logger_files/{tg_id}"
        await message.download_media(path)
        message_text = path
    elif event.message.is_reply:
        reply = await event.message.get_reply_message()
        reply_message.append(reply)
        reply_message.append(message)
        reply_mes_id = reply.id
        message_text = event.message.message
        tg_id = event.message.id

    if event.message.is_reply:
        await client.forward_messages(SAVE, reply_message)
        reply_message.clear()
    else:
        await client.forward_messages(SAVE, message)

    database.new_message(date, time, sender_id, tg_id, message_text, reply_mes_id)
    users = await client.get_participants(CHAT)
    update_users(users)
    database.commit()


client.run_until_disconnected()
