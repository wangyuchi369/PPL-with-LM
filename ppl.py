from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizerFast
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import json
import torch
from tqdm import tqdm
import timeit
import math
import os
#%%
# USE_CUDA = torch.cuda.is_available()
device = torch.device("cuda:1")
# os.environ['CUDA_VISIBLE_DEVICE']='1'
model_id = 'gpt2-medium'
model = GPT2LMHeadModel.from_pretrained(model_id).to(device)
# model = torch.nn.DataParallel(model, device_ids=[0, 1])

tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
#%%
def ppl(answer, statement):
    sentence = statement.replace('**blank**', answer)
    # sentence = answer + 'is the answer of question ' + statement
    encodings = tokenizer(sentence, return_tensors='pt')
    input_ids = encodings.input_ids.to(device)
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        cross_entropy = outputs[0] * encodings.input_ids.size(1)
    ppl = cross_entropy
    return ppl
#%%
answer_file = 'a.json'
statement_file = 'candidates.json'
with open(answer_file,'r') as f:
    answer_list = json.load(f).values()
with open(statement_file, 'r') as f:
    statement_struct = json.load(f)
    questions_list = statement_struct['questions']
#%%
start=timeit.default_timer()

for question in tqdm(questions_list[200000:202500]):
    question.pop('vilt_top100_answers')
    statement = question['statement']
    res = dict()
    for each_answer in answer_list:
        res[each_answer] = ppl(each_answer,statement)
    sort = sorted(res.items(),key=lambda x:x[1])[0:100]
    question['ppl_top100_answers'] = [answer[0] for answer in sort ]
end=timeit.default_timer()
with open('output/output21-1-1.json', 'w') as f:
    json.dump(statement_struct, f, indent =2)

print('Running time: %s Seconds'%(end-start))





