import json

def load_config(file_path):
    with open(file_path + "_config.json", 'r') as file:
        data = json.load(file)
    return data

# the input_sequence for the sentence "I have a dog" will now contain [["i", "have"], ["i", "have", "a"], ["i", "have", "a", "dog"]]
def generate_sequences(tokenizer, corpus):
    input_sequences = []
    for line in corpus: #each line will be sequenced and used as one example of "correct sentence"

        token_list = tokenizer.texts_to_sequences([line])[0] # create a token list for the sentence

        for i in range(1, len(token_list)): # Go through each token sequentially
            n_gram_sequence = token_list[:i+1] # the n_gram is the range of tokens from 1-(i + 1) 
            input_sequences.append(n_gram_sequence)
    return input_sequences
