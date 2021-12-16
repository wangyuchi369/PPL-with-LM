import math
import torch
from pytorch_pretrained_bert import OpenAIGPTTokenizer, OpenAIGPTModel, OpenAIGPTLMHeadModel
from tqdm import tqdm
import timeit
import json
#%%
# Load pre-trained model (weights)
model = OpenAIGPTLMHeadModel.from_pretrained('openai-gpt').to('cuda')
model.eval()
# Load pre-trained model tokenizer (vocabulary)
tokenizer = OpenAIGPTTokenizer.from_pretrained('openai-gpt')
#%%
def score(sentence):
    tokenize_input = tokenizer.tokenize(sentence)
    tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)]).to('cuda')
    loss=model(tensor_input, lm_labels=tensor_input)
    return math.exp(loss)

#%%
def ppl(answer, statement):
    sentence = statement.replace('**blank**', answer)
    return score(sentence)
answer_file = '../a.json'
statement_file = '../b.json'
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
with open('c.json', 'w') as f:
    json.dump(statement_struct, f, indent =2)
end=timeit.default_timer()
print('Running time: %s Seconds'%(end-start))

