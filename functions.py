import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r"i'm", "i am", text)
    text = re.sub(r"he's", "he is", text)
    text = re.sub(r"she's", "she is", text)
    text = re.sub(r"that's", "that is", text)
    text = re.sub(r"what's", "what is", text)
    text = re.sub(r"where's", "where is", text)
    text = re.sub(r"\'ll", " will", text)
    text = re.sub(r"\'ve", " have", text)
    text = re.sub(r"\'re", " are", text)
    text = re.sub(r"\'d", " would", text)
    text = re.sub(r"won't", "will not", text)
    text = re.sub(r"can't", "cannot", text)
    text = re.sub(r"[!-()\"#/@;:<>{}+=~|.?,]", "", text)
    return text

def get_bag(question, words2int):
    question = clean_text(question)
    bag = []
    for b in range(50):
        bag.append(0)
    i = 0
    for word in question.split():
        index = words2int.get(word)
        if index is None:
            index = len(words2int) + 1
            words2int[word] = index
        bag[i] = index
        i+=1
    return bag