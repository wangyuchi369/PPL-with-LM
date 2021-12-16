from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizerFast
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
import torch
from tqdm import tqdm
import timeit
import math
#%%
model_id = 'gpt2-medium'
model = GPT2LMHeadModel.from_pretrained(model_id).to('cuda')
tokenizer = GPT2Tokenizer.from_pretrained(model_id)
#%%
max_length = model.config.n_positions
stride = 1
sentence = 'the people in the background are doing me'
#sentence = answer +'is the answer of question' + statement
encodings = tokenizer(sentence, return_tensors='pt')
print(encodings)
nlls = []
for i in range(1, encodings.input_ids.size(1), stride):
    begin_loc = max(i + stride - max_length, 0)
    end_loc = min(i + stride, encodings.input_ids.size(1))
    trg_len = end_loc - i    # may be different from stride on last loop
    input_ids = encodings.input_ids[:,begin_loc:end_loc].to('cuda')
    target_ids = input_ids.clone()
    target_ids[:,:-trg_len] = -100

    with torch.no_grad():
        outputs = model(input_ids, labels=target_ids)
        neg_log_likelihood = outputs[0] * trg_len
    nlls.append(neg_log_likelihood)
ppl = torch.exp(torch.stack(nlls).sum())
#%%

print(nlls)
print(ppl)
