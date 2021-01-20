import json
import numpy as np
import tensorflow as tf
import tflearn
from functions import clean_text, get_bag

data = []

with open("response.json") as f:
    d = json.load(f)
    for s in d["data"]:
        data.append(s)

types = [d["type"] for d in data]
types2int = {types[i]: i for i in range(0, len(types))}
int2types = {v: k for k, v in types2int.items()}

train_x = []
train_y = []
words2int = {}
    
i = 1
for d in data:
    for question in d["questions"]:
        question = clean_text(question)
        for word in question.split():
            word = clean_text(word)
            if words2int.get(word) is None:
                words2int[word] = i
                i += 1
            

for d in data:
    for question in d["questions"]:
        train_x.append(get_bag(question, words2int))
        output = []
        for i in range(len(types2int)):
            output.append(0)
        output[types2int[d["type"]]] = 1
        train_y.append(output)
        
train_x = np.array(train_x)
train_y = np.array(train_y)

tf.compat.v1.reset_default_graph()

net = tflearn.input_data(shape=[None, len(train_x[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.dropout(net, 0.4)
net = tflearn.fully_connected(net, 8)
net = tflearn.dropout(net, 0.4)
net = tflearn.fully_connected(net, len(train_y[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)

model.fit(train_x, train_y, n_epoch=1000, batch_size=8, show_metric=True)
model.save('models/model.tflearn')

with open('data.json', 'w') as f:
    dump_data = {}
    dump_data["words2int"] = words2int
    dump_data["types2int"] = types2int
    dump_data["int2types"] = int2types
    
    json.dump(dump_data, f)