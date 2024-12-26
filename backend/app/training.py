import os
import random
import json
import pickle
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import Sequential # type: ignore
from tensorflow.keras.optimizers import SGD # type: ignore
from tensorflow.keras.layers import Dense, Conv1D, Embedding, MaxPooling1D, LSTM, Dropout # type: ignore


# Suppress TensorFlow warnings and force CPU usage
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow warnings
os.environ['CUDA_VISIBLE_DEVICES'] = ''  # Force TensorFlow to use CPU

# Ensure NLTK data is downloaded and paths are configured
nltk.data.path.append('/root/nltk_data')
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

# Attempt to download punkt_tab (might not exist in all NLTK versions)
try:
    nltk.download('punkt_tab')
except LookupError:
    print("punkt_tab not available; continuing with default punkt tokenizer.")

# Initialize lemmatizer and constants
lemmatizer = WordNetLemmatizer()
ignore_letters = ['?', '!', '.', '/', '@']

# Load intents.json
try:
    intents_path = os.path.join(os.getcwd(), 'intents.json')
    with open(intents_path, 'r') as file:
        intents = json.load(file)
except FileNotFoundError as e:
    raise FileNotFoundError(f"Could not find 'intents.json' in the current directory: {os.getcwd()}") from e

# Initialize data structures for processing
words = []
classes = []
documents = []

# Tokenize and process patterns in intents
for intent in intents['intents']:
    for pattern in intent['patterns']:
        word_list = nltk.word_tokenize(pattern)  # Explicitly tokenize without punkt_tab
        words.extend(word_list)
        documents.append((word_list, intent['tag']))
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Remove ignore letters and lemmatize
stop_words = set(stopwords.words('english'))
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in ignore_letters]
words = sorted(set(words))
classes = sorted(set(classes))

# Save processed data
output_dir = os.getcwd()
pickle.dump(words, open(os.path.join(output_dir, 'words.pkl'), 'wb'))
pickle.dump(classes, open(os.path.join(output_dir, 'classes.pkl'), 'wb'))

# Create training data
training = []
output_empty = [0] * len(classes)

for document in documents:
    bag = []
    word_patterns = document[0]
    word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
    for word in words:
        bag.append(1) if word in word_patterns else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(document[1])] = 1
    training.append([bag, output_row])

# Shuffle and convert to numpy arrays
random.shuffle(training)
training = np.array(training, dtype=object)
train_x = list(training[:, 0])
train_y = list(training[:, 1])
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


# Train the model
try:
    hist = model.fit(np.array(train_x), np.array(train_y), epochs=200, batch_size=5, verbose=1)
except Exception as e:
    raise RuntimeError("Error occurred during model training.") from e

# Save the trained model
model_path = os.path.join(output_dir, 'chatbot_model.keras')
model.save(model_path)

print(f"Training completed. Model saved to: {model_path}")
