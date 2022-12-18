from transformers import BertTokenizer, BertForSequenceClassification

import numpy as np


class Sentiment:
    model = 'yiyanghkust/finbert-tone'

    finbert = BertForSequenceClassification.from_pretrained(
        model, num_labels=3)

    tokenizer = BertTokenizer.from_pretrained(model)

    labels = {0: 'neutral', 1: 'positive', 2: 'negative'}

    def run(self, sentences):
        inputs = self.tokenizer(sentences, return_tensors="pt", padding=True)
        outputs = self.finbert(**inputs)[0]

        result = []

        for idx, sent in enumerate(sentences):
            label = self.labels[np.argmax(outputs.detach().numpy()[idx])]
            print(sent, '----', label)
            result.push((sent, label))

    def coverage_test():
        print("COVTEST")
