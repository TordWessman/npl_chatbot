#!env/bin/python3
import asyncio
from datetime import datetime, timedelta
from telethon import TelegramClient, events
import time
import sqlite3
import re
from shared import load_config

def split_shit(string, delimiters, exceptions):
    pattern = '|'.join(f'(?<!{re.escape(exception)})[{re.escape(delimiters)}]' for exception in exceptions)
    return re.split(pattern, string)

secret_config = load_config("secret")
config = load_config("shared") 
api_id = secret_config["api_id"]
api_hash = secret_config["api_hash"]
phone_number = secret_config["api_phone"]
db_name = config["db_name"]
group_name = config["group_name"]
min_sentence_length = 3
max_sentence_length = 30
bad_chars = "'%"
split_exceptions = ['t.ex.', "etc."]

conn = sqlite3.connect(db_name)

def start():
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS sentence (id INTEGER PRIMARY KEY, text TEXT)")
    conn.commit()

def add_sentence(sentence):
    c = conn.cursor()
    c.execute(f"INSERT INTO sentence (text) VALUES (\"{sentence}\")")
    conn.commit()

async def get_group_messages():
    client = TelegramClient('session_name', api_id, api_hash)
    await client.connect()

    if not await client.is_user_authorized():
        await client.send_code_request(phone_number)
        await client.sign_in(phone_number, input('Enter the code: '))

    group = await client.get_entity(group_name)
    messages = []
    
    async for message in client.iter_messages(group, min_id=1):
        time.sleep(0.1)
        delimiters = '.'
        
        if message.message:
            for msg_row in message.message.split('\n'):
                for spt in split_shit(msg_row, delimiters, split_exceptions):
                    spt = spt.replace(bad_chars, '')
                    spt = re.sub(r'["“”]', '', spt).strip()
                    word_count = len(spt.split(' '))
                    if word_count <= max_sentence_length and word_count >= min_sentence_length:
                        messages.append(spt)
    return messages

start()
messages = asyncio.run(get_group_messages())

for sentence in messages:
    print("--------------------------")
    print(sentence)
    add_sentence(sentence)

conn.close()