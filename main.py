import tflearn
import tensorflow as tf
import json
import random
import numpy as np
from functions import get_bag

int2types = {}
types2int = {}
words2int = {}
data = []

with open("response.json") as f:
    d = json.load(f)
    for s in d["data"]:
        data.append(s)

with open('data.json') as f:
    dump_data = json.load(f)
    int2types = dump_data["int2types"]
    types2int = dump_data["types2int"]
    words2int = dump_data["words2int"]

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, 50])
net = tflearn.fully_connected(net, 8)
net = tflearn.dropout(net, 0.4)
net = tflearn.fully_connected(net, 8)
net = tflearn.dropout(net, 0.4)
net = tflearn.fully_connected(net, len(int2types), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.load('models/model.tflearn')

        
while True:
    prediction = model.predict(np.array([get_bag(input("Text: "), words2int)]))
    result = int2types[str(np.argmax(prediction))]
    
    for d in data:
        if d["type"] == result:
            answers = d["answers"]
            print("Response:",answers[random.randint(0, len(answers)-1)])










