#!env/bin/python3
from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, filters, MessageHandler
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import sqlite3
import numpy as np
from shared import load_config, generate_sequences
import random

secrets = load_config("secret")
config = load_config("shared")
db_name = config["db_name"]
model_name = config["model_name"]
min_answer_len = 5
max_answer_len = 15
command_name = "din_mamma"
random_seed_count = 3 # must not be greater than 3, because it's hardcoded in the scraper!

conn = sqlite3.connect(db_name)

def get_sentences():
    c = conn.cursor()
    c.execute("SELECT text FROM sentence")
    return [row[0].lower() for row in c.fetchall()]

corpus = get_sentences()

tokenizer = Tokenizer()
tokenizer.fit_on_texts(corpus)
model = tf.keras.models.load_model(model_name)

input_sequences = generate_sequences(tokenizer, corpus)
max_sequence_len = max([len(x) for x in input_sequences])

def create_answer(seed_text, reply_word_count):
    for _ in range(reply_word_count):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
        predicted = np.argmax(model.predict(token_list), axis=-1)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

def get_random_seed_text():
    sentence = random.choice(corpus)
    words = sentence.split() 
    return ' '.join(words[:random_seed_count])

async def din_mamma(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    input_text = update.message.text.strip(f"/{command_name}").strip()
    if input_text and len(input_text):
        reply_text = create_answer(input_text, random.randint(min_answer_len, max_answer_len))
    else:
        reply_text = create_answer(get_random_seed_text(), random.randint(min_answer_len, max_answer_len))

    await update.message.reply_text(f'{update.effective_user.first_name}: {reply_text}')

app = ApplicationBuilder().token(secrets["bot_token"]).build()

app.add_handler(CommandHandler(command_name, din_mamma))

app.run_polling()