import multiprocessing
from multiprocessing import Pool
import os, time
from transformers import OpenAIGPTLMHeadModel, OpenAIGPTTokenizerFast
from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import json
import torch
from tqdm import tqdm
import timeit
import math


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
def myf(question_slice):
    with open('a.json','r') as f:
        answer_list = json.load(f).values()
    a = question_slice.copy()
    for question in tqdm(a):
        question.pop('vilt_top100_answers')
        statement = question['statement']
        res = dict()
        for each_answer in answer_list:
            res[each_answer] = ppl(each_answer,statement)
        sort = sorted(res.items(),key=lambda x:x[1])[0:100]
        question['ppl_top100_answers'] = [answer[0] for answer in sort ]
    return a
#%%
if __name__ == '__main__':
    multiprocessing.set_start_method('forkserver', force=True)

    print('Parent process %s.' % os.getpid())
    USE_CUDA = torch.cuda.is_available()
    device = torch.device("cuda:0" if USE_CUDA else "cpu")
    model_id = 'gpt2-medium'
    model = GPT2LMHeadModel.from_pretrained(model_id)
    model.to(device)
    tokenizer = GPT2TokenizerFast.from_pretrained(model_id)


    statement_file = 'b.json'

    with open(statement_file, 'r') as f:
        statement_struct = json.load(f)
        questions_list = statement_struct['questions']
    step = 3
    n = len(questions_list)
    start=timeit.default_timer()
    slice = [questions_list[i:min(n,i+step)] for i in range(0,n,step)]
    with Pool(5) as p:
        p.map(myf, slice)
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')