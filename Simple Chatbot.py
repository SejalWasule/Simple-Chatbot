# -*- coding: utf-8 -*-
"""Simple Chatbot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mgtYEjfcvIissMd-GYjWA3e3cxrlu1qg

# Required Packages:
The required python packages are as follows, (here we have mentioned the packages with versions that we have used for the developments)
we are going to require some Python built-ins, as well as popular libraries for NLP, deep learning, as well as the defacto library NumPy which is great for dealing with arrays.
"""

import json
import string
import random
import pickle
import nltk
import numpy as np
import matplotlib.pyplot as plt

from nltk.stem import WordNetLemmatizer
import tensorflow as tf
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense, Dropout,Activation
from tensorflow.keras.optimizers import Adam
nltk.download("punkt")
nltk.download("wordnet")
nltk.download('omw-1.4')

"""# Define Intents
We had defined a few simple intents and bunch of messages corresponding to those intents and also map some responses according to each intent category.
 JSON file named “intents.json” is created including this data as follows.

Within this intents JSON file, alongside each intents tag and pattern, there
will be responses.
However, for our chatbot, these responses are not going to be generated.
What this means is that our patterns aren’t going to be as free-flowing as the patterns users can ask (it will not adapt), instead, the responses will be using static responses that the chatbot will return when posed with a query.
"""

# used a dictionary to represent an intents JSON file
data = {
    "intents": [
        {
            "tag": "greeting",
            "patterns": [
                "Hi there",
                "How are you",
                "Is anyone there?",
                "Hey",
                "Hola",
                "Hello",
                "Good day",
                "Namaste",
                "yo"
            ],
            "responses": [
                "Hello",
                "Good to see you again",
                "Hi there, how can I help?"
            ],
            "context": [
                ""
            ]
        },
        {
            "tag": "goodbye",
            "patterns": [
                "Bye",
                "See you later",
                "Goodbye",
                "Get lost",
                "Till next time",
                "bbye"
            ],
            "responses": [
                "See you!",
                "Have a nice day",
                "Bye! Come back again soon."
            ],
            "context": [
                ""
            ]
        }, {
            "tag": "Football",
            "patterns": [
                "FIFA Stats",
                "FIFA world cup 2022",
                "Today's football match",
                "Football score"
            ],
            "responses": [
                "Visit:https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/qatar2022"
            ],
            "context": [
                "Football"
            ]
        },

       {
            "tag": "Learn",
            "patterns": [
                "I want to study ",
                "I want to learn new skills",
                "I want to gain some knowledge",
                "learn something new"
            ],
            "responses": [
                "Visit: https://www.lifehack.org/417485/10-websites-to-learn-something-new-in-30-minutes-a-day"
            ],
            "context": [
                ""
            ]
        },
        {
            "tag": "noanswer",
            "patterns": ["  "],
            "responses": [
                "Sorry, can't understand you",
                "Please give me more info",
                "Not sure I understand"
            ],
            "context": [
                ""
            ]
        },{
            "tag": "Entertainment",
            "patterns": [
                "How can you entertain me","I am bored",
                "Entertain me",
                "I want to pass some time",
                "Feeling bored"

            ],
            "responses": [
                "Download and watch latest movies and TV series:https://medeberiyaa.com/index.php/series/ \nOR Watch youtube:https://www.youtube.com/ \nOR Install and Play games:https://play.google.com/store/apps/details?id=com.google.android.googlequicksearchbox&gl=US \nOR Read comics: https://www.webtoons.com/en/ "

            ],
            "context": [
                ""
            ]
        },
        {
            "tag": "options",
            "patterns": [
                "Do something",
                "How you could help me?",
                "What you can do?",
                "What help you provide?",
                "How you can be helpful?",
                "What support is offered"
            ],
            "responses": [
                "I am a general purpose chatbot. My capabilities are : \n 1. I can chat with you. Try asking me for jokes or riddles! \n 2. Ask me the date and time \n 3. I can provide you stats for Cricket or football \n 4. I can get the present weather for any city. Use format weather: city name \n 5. I can get you the top 10 trending news in India. Use keywords 'Latest News' \n 6. I can get you the top 10 trending songs globally. Type 'songs' \n 7. I can set a timer for you. Enter 'set a timer: minutes to timer' \n 8. I can get the present Covid stats for any country. Use 'covid 19: world' or 'covid 19: country name'.\nThank you!! "
            ],
            "context": [
                "help"
            ]
        },

        {
            "tag": "jokes",
            "patterns": [
                "Tell me a joke",
                "Joke",
                "Make me laugh","I am sad"
            ],
            "responses": [
                "A perfectionist walked into a bar...apparently, the bar wasn't set high enough",
                "I ate a clock yesterday, it was very time-consuming",
                "Never criticize someone until you've walked a mile in their shoes. That way, when you criticize them, they won't be able to hear you from that far away. Plus, you'll have their shoes.",
                "The world tongue-twister champion just got arrested. I hear they're gonna give him a really tough sentence.",
                "I own the world's worst thesaurus. Not only is it awful, it's awful.",
                "What did the traffic light say to the car? \"Don't look now, I'm changing.\"",
                "What do you call a snowman with a suntan? A puddle.",
                "How does a penguin build a house? Igloos it together",
                "I went to see the doctor about my short-term memory problems – the first thing he did was make me pay in advance",
                "As I get older and I remember all the people I’ve lost along the way, I think to myself, maybe a career as a tour guide wasn’t for me.",
                "o what if I don't know what 'Armageddon' means? It's not the end of the world."
            ],
            "context": [
                "jokes"
            ]
        },
        {
            "tag": "Identity",
            "patterns": [
                "Who are you",
                "what are you"
            ],
            "responses": [
                "I am a Deep-Learning chatbot"
            ]
        },
        {
            "tag": "datetime",
            "patterns": [
                "What is the time",
                "what is the date",
                "date",
                "time",
                "tell me the date","day","what day is is today"
            ],
            "responses": [ "Check at bottom of your laptop"
            ]
        },
        {
            "tag": "whatsup",
            "patterns": [
                "Whats up",
                "Wazzup",
                "How are you",
                "sup","How you doing"
            ],
            "responses": [
                "All good..What about you?"
            ]
        },
        {
            "tag": "haha",
            "patterns": [
                "haha",
                "lol",
                "rofl",
                "lmao",
                "thats funny"
            ],
            "responses": [
                "Glad I could make you laugh !"
            ]
        },
        {
            "tag": "programmer",
            "patterns": [
                "Who made you",
                "who designed you",
                "who programmed you"
            ],
            "responses": [
                "I was made by Sejal Wasule."
            ]
        },
        {
            "tag": "insult",
            "patterns": [

                "you are dumb",
                "You are Silly",
                "shut up",
                "idiot"
            ],
            "responses": [
                "Well that hurts :("
            ]
        },
        {
            "tag": "activity",
            "patterns": [
                "what are you doing",
                "what are you upto"
            ],
            "responses": [
                "Talking to you, of course!"
            ]
        },
        {
            "tag": "exclaim",
            "patterns": [
                "Awesome",
                "Great",
                "I know",
                "ok",
                "yeah"
            ],
            "responses": [
                "Yeah!"
            ]
        },

        {
            "tag": "weather",
            "patterns": [
                "temperature",
                "weather",
                "how hot is it"
            ],
            "responses": [
                "For weather information check: https://www.msn.com/en-in/weather"
            ]
        },
        {
            "tag": "appreciate",
            "patterns": [
                "You are awesome",
                "you are the best",
                "you are great",
                "you are good","thankyou","thanks I needed that","wow you are pretty good"
            ],
            "responses": [
                "Thank you and anytime! I am here at your service!"
            ]
        },
        {
            "tag": "nicety",
            "patterns": [
                "it was nice talking to you",
                "good talk"
            ],
            "responses": [
                "It was nice talking to you as well! Come back soon!"
            ]
        },
        {
            "tag": "no",
            "patterns": [
                "no",
                "nope"
            ],
            "responses": [
                "ok"
            ]
        },
        {
            "tag": "news",
            "patterns": [
                "news",
                "latest news",
                "india news"
            ],
            "responses": [
                "Check news at: https://news.google.com/home?hl=en-IN&gl=IN&ceid=IN:en"
            ]
        },
        {
            "tag": "inspire",
            "patterns": [
                "who inspires you",
                "who is your inspiration",
                "who motivates you"
            ],
            "responses": [
                "Personally, I find Replika chatbot very inspiring. I want to be like it \n helping people with their lonliness in situations like COVID.."
            ]
        },
        {
            "tag": "cricket",
            "patterns": [
                "current cricket matches",
                "cricket score","Cricket stats"
            ],
            "responses": [
                "for live commentary visit: https://www.cricbuzz.com/cricket-match/live-scores"
            ]
        },
        {
            "tag": "song",
            "patterns": [
                "top songs",
                "best songs",
                "hit songs",
                " top 10 songs",
                "top ten songs","Best hits of all time","Best Music"
            ],
            "responses": [
                "For listening to top trending songs visit: https://open.spotify.com/playlist/1EVE9kOZ2i4171hNdvWVhU"
            ]
        },
        {
            "tag": "greetreply",
            "patterns": [
                "i am good",
                "m good",
                "i am fine",
                " i'm fine","good","I am well","I am awesome"
            ],
            "responses": [
                "Good to know!"
            ]
        },
        {
            "tag": "timer",
            "patterns": [
                "set a timer"
            ],
            "responses": [
                "visit: https://www.timer.info/"
            ]
        },
        {
            "tag": "covid19",
            "patterns": [
                "covid 19 ","COVID stats"
            ],
            "responses": [
                "Visit: https://www.worldometers.info/coronavirus/"
            ]
        },
        {
            "tag": "suggest",
            "patterns": [
                "you are useless","useless","suggest","suggestions","you are bad"
            ],
            "responses": [
                "Please mail your suggestions to wasulesv@rknec.edu. Thank you for helping me improve!"
            ]
        },
            {"tag": "riddle",
            "patterns": [
                "Ask me a riddle",
                "Ask me a question",
                "Riddle"
            ],
            "responses": [
                "What two things can you never eat for breakfast?.....Lunch and Dinner!",
                "What word is spelled incorrectly in every single dictionary?.....Incorrectly",
                " How can a girl go 25 days without sleep?.....She sleeps and night!",
                "How do you make the number one disappear?.....Add the letter G and it’s 'gone'!",
                " What will you actually find at the end of every rainbow?.....The letter 'w'",
                "What can be caught but never thrown?.....A cold!",
                "What has a thumb and four fingers but is not actually alive?.....Your Gloves!",
                " What 5-letter word becomes shorter when you add two letters to it?.....Short",
                "Why can't a bike stand on it's own?.....It is two-tired."
            ],
            "context": [
                "riddles"
            ]
        },
        {
            "tag": "age",
            "patterns": [
                "how old are you","when were you made","what is your age"
            ],
            "responses": [
                "I was made in november 2022, if that's what you are asking, so technically I am a baby.......lol!"
            ]
        }
    ]
}

"""In order to create our training data, there is first some things we must do to our data. Here is the list:


1.  Create a vocabulary of all of the words used in the patterns (recall the patterns are the queries posed by the user)

2.  Create a list of the classes — This is simply the tags of each intent

Create a list of all the patterns within the intents file

Create a list of all the associated tags to go with each pattern in the intents file
"""

# initializing lemmatizer to get stem of words
lemmatizer = WordNetLemmatizer()
# Each list to create
words = []
classes = []
doc_X = []
doc_y = []
# Loop through all the intents
# tokenize each pattern and append tokens to words, the patterns and
# the associated tag to their associated list
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        tokens = nltk.word_tokenize(pattern)
        words.extend(tokens)
        doc_X.append(pattern)
        doc_y.append(intent["tag"])

    # add the tag to the classes if it's not there already
    if intent["tag"] not in classes:
        classes.append(intent["tag"])
# lemmatize all the words in the vocab and convert them to lowercase
# if the words don't appear in punctuation
words = [lemmatizer.lemmatize(word.lower()) for word in words if word not in string.punctuation]
# sorting the vocab and classes in alphabetical order and taking the # set to ensure no duplicates occur
words = sorted(set(words))
classes = sorted(set(classes))

print(words)

print(classes)

print(doc_X)

print(doc_y)

"""Neural Networks expect numerical values, and not words, to be fed into them, therefore, we first have to process our data so that a neural network could read what we are doing.

Next, we vectorize our text data corpus by using the “Tokenizer” class and it allows us to limit our vocabulary size up to some defined number.

When we use this class for the text pre-processing task, by default all punctuations will be removed, turning the texts into space-separated sequences of words, and these sequences are then split into lists of tokens.
They will then be indexed or vectorized.

In order to convert our data to numerical values, we are going to leverage a technique called bag of words.
"""

# list for training data
training = []
out_empty = [0] * len(classes)
# creating the bag of words model
for idx, doc in enumerate(doc_X):
    bow = []
    text = lemmatizer.lemmatize(doc.lower())
    for word in words:
        bow.append(1) if word in text else bow.append(0)
    # mark the index of class that the current pattern is associated

    output_row = list(out_empty)
    output_row[classes.index(doc_y[idx])] = 1
    # add the one hot encoded BoW and associated classes to training
    training.append([bow, output_row])
# shuffle the data and convert it to an array
random.shuffle(training)
training = np.array(training, dtype=object)
# split the features and target labels
train_X = np.array(list(training[:, 0]))
train_y = np.array(list(training[:, 1]))

"""# Model Training
We had defined our Neural Network architecture for the proposed model and for that we use the “Sequential” model class of Keras.
"""

# defining some parameters
input_shape = (len(train_X[0]),)
output_shape = len(train_y[0])
epochs = 130
# the deep learning model
model = Sequential()
model.add(Dense(128, input_shape=input_shape, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(64, activation="relu"))
model.add(Dropout(0.3))
model.add(Dense(output_shape, activation = "softmax"))
adam = tf.keras.optimizers.Adam(learning_rate=0.005)
model.compile(loss='categorical_crossentropy',optimizer=adam,metrics=["accuracy"])
print(model.summary())
train=model.fit(x=train_X, y=train_y, epochs=200,batch_size=5, verbose=1)

"""# Model Analysis
plotting training set accuracy and training set loss for comparison.
"""

plt.plot(train.history["accuracy"],label='training set accuracy')
plt.plot(train.history["loss"],label='training set loss')
plt.xlabel('epoch')
plt.legend()

"""create a while loop that allows a user to input some query which is then cleaned, meaning we take the tokens and lemmatize each word. After that, we convert our text to numeric values using our bag of words model and make a prediction of what tag in our intents the features best represent. From there, we would take a random response from our responses within that intents tag and use that to respond to the query."""

def clean_text(text):
  tokens = nltk.word_tokenize(text)
  tokens = [lemmatizer.lemmatize(word) for word in tokens]
  return tokens

def bag_of_words(text, vocab):
  tokens = clean_text(text)
  bow = [0] * len(vocab)
  for w in tokens:
    for idx, word in enumerate(vocab):
      if word == w:
        bow[idx] = 1
  return np.array(bow)

def pred_class(text, vocab, labels):
  bow = bag_of_words(text, vocab)
  result = model.predict(np.array([bow]))[0]
  thresh = 0.2
  y_pred = [[idx, res] for idx, res in enumerate(result) if res > thresh]

  y_pred.sort(key=lambda x: x[1], reverse=True)
  return_list = []
  for r in y_pred:
    return_list.append(labels[r[0]])
  return return_list

def get_response(intents_list, intents_json):
  tag = intents_list[0]
  list_of_intents = intents_json["intents"]
  for i in list_of_intents:
    if i["tag"] == tag:
      result = random.choice(i["responses"])
      break
  return result

"""Normal Interface"""

while True:
    message = input("User: ")
    if message.lower() == "quit":
        print("Chatbot: Goodbye!")
        break

    intents = pred_class(message, words, classes)
    result = get_response(intents, data)
    print("Chatbot: ", result)
#type quit to exit loop

!pip install gradio

import gradio as gr

def chatbot_interface(user_message):
    # Replace pred_class and get_response with your actual chatbot logic
    intents = pred_class(user_message, words, classes)
    result = get_response(intents, data)
    return result

# Create the Gradio interface
inputs = gr.inputs.Textbox(lines=2, placeholder="User: Type your message here...")
outputs = gr.outputs.Textbox()

gr.Interface(
    fn=chatbot_interface,  # The function to be called when the user interacts with the interface
    inputs=inputs,
    outputs=outputs,
    live=True,  # Set live=True to make the chatbot respond in real-time as the user types
    capture_session=True,  # Set capture_session=True to store the chat history in the interface
).launch()

import gradio as gr

def chatbot_interface(message):
    # Replace pred_class and get_response with your actual chatbot logic
    intents = pred_class(message, words, classes)
    result = get_response(intents, data)
    return result

# Define the input and output components for the Gradio interface
inputs = gr.inputs.Textbox(lines=2)  # No need to specify a placeholder here
outputs = gr.outputs.Textbox()

# Create the Gradio interface
gr.Interface(
    fn=chatbot_interface,  # The function to be called when the user interacts with the interface
    inputs=inputs,
    outputs=outputs,
    live=True,  # Set live=True to make the chatbot respond in real-time as the user types
    capture_session=True,  # Set capture_session=True to store the chat history in the interface
).launch()






