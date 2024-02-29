#!env/bin/python3
from webbrowser import MacOSX
import tensorflow as tf

from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, LSTM, Dense, Bidirectional
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential
#from tensorflow.keras.optimizers import Adam
from tensorflow.keras.optimizers.legacy import Adam # Works best om M1 / M2
import numpy as np 
import sqlite3
from shared import load_config, generate_sequences

train = True
config = load_config("shared")
db_name = config["db_name"]
model_name = config["model_name"]

conn = sqlite3.connect(db_name)

def get_sentences():
    c = conn.cursor()
    c.execute("SELECT text FROM sentence")
    return [row[0].lower() for row in c.fetchall()]

corpus = get_sentences()

tokenizer = Tokenizer()

tokenizer.fit_on_texts(corpus)
total_words = len(tokenizer.word_index) + 1 # add one zero-token

model = None

if not train:
    model = tf.keras.models.load_model(model_name)

#print(tokenizer.word_index)
#print(total_words)

input_sequences = generate_sequences(tokenizer, corpus)

# pad sequences 
max_sequence_len = max([len(x) for x in input_sequences]) # Determine the max sequence length
padded_sequences = pad_sequences(input_sequences, maxlen=max_sequence_len, padding='pre') # Make sure each sequence has the same length by padding `0` if len < max_sequence_len
input_sequences = np.array(padded_sequences) # convert to a np array

if train:
    # create predictors and label
    xs, labels = input_sequences[:,:-1],input_sequences[:,-1]
    # The labels is the last word in the current sequence. So "I have a dog" will generate the label "dog" and "I have a" will generate the label "a"

    ys = tf.keras.utils.to_categorical(labels, num_classes=total_words) #the labels will be categorically one-hot encoded into the "train labels" (y:s)

    # Here be magic model
    model = Sequential()
    number_of_dimensions = 100
    model.add(Embedding(total_words, number_of_dimensions, input_length=max_sequence_len-1))
    model.add(Bidirectional(LSTM(150)))
    model.add(Dense(total_words, activation='softmax'))
    adam = Adam(learning_rate=0.01)
    model.compile(loss='categorical_crossentropy', optimizer=adam, metrics=['accuracy'])

    #earlystop = EarlyStopping(monitor='val_loss', min_delta=0, patience=5, verbose=0, mode='auto')
    history = model.fit(xs, ys, epochs=100, verbose=1)
    #print model.summary()
    print(model)
    print(history)
    model.save(model_name)

seed_text = "gissar på att"
next_words = 100
  
for _ in range(next_words):
	token_list = tokenizer.texts_to_sequences([seed_text])[0]
	token_list = pad_sequences([token_list], maxlen=max_sequence_len-1, padding='pre')
	predicted = np.argmax(model.predict(token_list), axis=-1)
	output_word = ""
	for word, index in tokenizer.word_index.items():
		if index == predicted:
			output_word = word
			break
	seed_text += " " + output_word
print(seed_text)
