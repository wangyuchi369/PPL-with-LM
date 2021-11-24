#%%
import numpy as np
import torch
import torch.nn as nn
from transformers import BertTokenizer, BertForMaskedLM
# Load pre-trained model (weights)

model = BertForMaskedLM.from_pretrained('bert-base-uncased').to('cuda')
# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
#%%
with torch.no_grad():
    sentence = "i am gaga happy"
    tokenize_input = tokenizer.tokenize(sentence)
    tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)])
    sen_len = len(tokenize_input)
    sentence_loss = 0.

    for i, word in enumerate(tokenize_input):
        # add mask to i-th character of the sentence
        tokenize_input[i] = '[MASK]'
        mask_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)])

        output = model(mask_input)

        prediction_scores = output[0]
        softmax = nn.Softmax(dim=0)
        ps = softmax(prediction_scores[0, i]).log()
        word_loss = ps[tensor_input[0, i]]
        sentence_loss += word_loss.item()

        tokenize_input[i] = word
    ppl = np.exp(-sentence_loss/sen_len)
    print(ppl)
