import random
import json
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model  # type: ignore

lemmatizer = WordNetLemmatizer()
intents = json.loads(open('C:/Users/rabia/OneDrive - Solent University/COM727-Assessment/ANNChatbot/ANNChatbot/intents.json').read())

# Load vocabulary and model
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbot_model.keras')

# Clean up the sentence
def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# Convert the sentence into a bag of words
def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

# Predict the intent class
def predict_class(sentence):
    bow = bag_of_words(sentence)
    

    # Check for empty input
    if np.sum(bow) == 0:
        return [{"intent": "no_match", "probability": "0"}]

    res = model.predict(np.array([bow]))[0]

    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({'intent': classes[r[0]], 'probability': str(r[1])})
    return return_list

# Get the response based on predicted intent
def get_response(intents_list, intents_json):
    if len(intents_list) == 0 or intents_list[0]['intent'] == "no_match":
        return "I'm sorry, I don't understand. Could you rephrase?"

    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

# Test the chatbot
while True:
    message = input("You: ")
    if message.lower() == "quit":
        break

    intents_list = predict_class(message)
    response = get_response(intents_list, intents)
    print(f"Bot: {response}")
