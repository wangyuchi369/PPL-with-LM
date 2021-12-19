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

def ppl(answer, statement):
    sentence = statement.replace('**blank**', answer)
    #sentence = answer +'is the answer of question' + statement
    encodings_statement = tokenizer(statement,return_tensors='pt').input_ids
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
    print(nlls)
    ppl = torch.exp(torch.stack(nlls).sum())
    return ppl
#%%
answer_file = '../anwers.json'
statement_file = '../question_examples.json'
with open(answer_file,'r') as f:
    answer_list = json.load(f).values()
with open(statement_file, 'r') as f:
    statement_struct = json.load(f)
    questions_list = statement_struct['questions']
start=timeit.default_timer()
for question in tqdm(questions_list[5:16]):
    question.pop('vilt_top100_answers')
    statement = question['statement']
    res = dict()
    for each_answer in answer_list:
        res[each_answer] = ppl(each_answer,statement)
    sort = sorted(res.items(),key=lambda x:x[1])[0:100]
    question['answer'] = [answer[0] for answer in sort ]
with open('c.json', 'w') as f:
    json.dump(statement_struct, f, indent =2)
end=timeit.default_timer()
print('Running time: %s Seconds'%(end-start))

#%%
ppl('spoon','**blank** is to the right of the soup')
#%%
ppl('bedroom','**blank** is to the right of the soup')




