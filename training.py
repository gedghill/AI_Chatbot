import random
import json
import pickle
import numpy as np
import nltk
import tensorflow as tf
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.layers import Dense, Conv1D, Embedding, MaxPooling1D, LSTM, Dropout # type: ignore

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()

# Load intents file
intents = json.loads(open('C:/Users/rabia/OneDrive - Solent University/COM727-Assessment/ANNChatbot/ANNChatbot/intents.json').read())

# Preprocessing
words = []
classes = []
documents = []
ignore_letters = ['?', '!', '.', '/', '@']

for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

stop_words = set(stopwords.words('english'))
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters and word not in stop_words]
words = sorted(set(words))

classes = sorted(set(classes))

# Save words and classes
pickle.dump(words, open('words.pkl', 'wb'))
pickle.dump(classes, open('classes.pkl', 'wb'))

# Training Data Preparation
training = []
output_empty = [0] * len(classes)
for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1 if word in word_patterns else 0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training, dtype=object)

train_x = np.array(list(training[:, 0]))  # Features
train_y = np.array(list(training[:, 1]))  # Labels

# CNN + LSTM Model
model = Sequential()

# Embedding Layer
model.add(Embedding(input_dim=len(words),  # Size of the vocabulary
                    output_dim=128,       # Embedding dimensions (e.g., 128)
                    input_length=len(train_x[0])))  # Length of each input sequence

# CNN Layer for Feature Extraction
model.add(Conv1D(filters=128, kernel_size=5, activation='relu'))
model.add(MaxPooling1D(pool_size=2))

# LSTM Layer for Sequential Learning
model.add(LSTM(128, return_sequences=False))

# Dense Layer for Classification
model.add(Dense(64, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(len(classes), activation='softmax'))  # Number of classes

# Compile the Model
model.compile(optimizer='adam', 
               loss='categorical_crossentropy', 
                metrics=['accuracy'])


hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
model.save('chatbot_model.keras', hist)

print("Training Complete!")

