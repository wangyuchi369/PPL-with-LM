from transformers import GPT2LMHeadModel, GPT2TokenizerFast
import json
import torch
from tqdm import tqdm
import timeit
#%%
model_id = 'gpt2'
model = GPT2LMHeadModel.from_pretrained(model_id).to('cuda')
tokenizer = GPT2TokenizerFast.from_pretrained(model_id)
#%%
def ppl(answer, statement):
    sentence = statement.replace('**blank**', answer)
    encodings = tokenizer(sentence, return_tensors='pt')
    input_ids = encodings.input_ids.to('cuda')
    with torch.no_grad():
        outputs = model(input_ids, labels=input_ids)
        cross_entropy = outputs[0]
    ppl = torch.exp(cross_entropy)
    return ppl
#%%
answer_file = 'a.json'
statement_file = 'b.json'
with open(answer_file,'r') as f:
    answer_list = json.load(f).values()
with open(statement_file, 'r') as f:
    statement_struct = json.load(f)
    questions_list = statement_struct['questions']
start=timeit.default_timer()
for question in tqdm(questions_list):
    question.pop('vilt_top100_answers')
    statement = question['statement']
    res = dict()
    for each_answer in answer_list:
        res[each_answer] = ppl(each_answer,statement)
    sort = sorted(res.items(),key=lambda x:x[1])[0:100]
    question['answer'] = [answer[0] for answer in sort ]
with open('c.json','w') as f:
    json.dump(statement_struct, f, indent =2)
end=timeit.default_timer()
print('Running time: %s Seconds'%(end-start))

#%%
ppl('down','he is looking **blank**')



