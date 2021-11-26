import numpy as np
import torch
from pytorch_pretrained_bert import BertTokenizer,BertForMaskedLM
# Load pre-trained model (weights)
import json
from tqdm import tqdm
import timeit
#%%
with torch.no_grad():
    model = BertForMaskedLM.from_pretrained('bert-large-cased').to('cuda')
    model.eval()
    # Load pre-trained model tokenizer (vocabulary)
    tokenizer = BertTokenizer.from_pretrained('bert-large-cased')
#%%
def ppl(answer,statement):
    return score(statement.replace('**blank**',answer))
def score(sentence):
    tokenize_input = tokenizer.tokenize(sentence)
    tensor_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)]).to('cuda')
    sentence_loss=0.
    for i,word in enumerate(tokenize_input):
        tokenize_input[i]='[MASK]'
        mask_input = torch.tensor([tokenizer.convert_tokens_to_ids(tokenize_input)]).to('cuda')
        word_loss=model(mask_input, masked_lm_labels=tensor_input).data
        sentence_loss +=word_loss
        #print("Word: %s : %f"%(word, np.exp(-word_loss)))
    return torch.exp(sentence_loss/len(tokenize_input))
#%%
print(score("the people in the background are doing noting"))
answer_file = 'a.json'
statement_file = 'b.json'
with open(answer_file,'r') as f:
    answer_list = json.load(f).values()
with open(statement_file, 'r') as f:
    statement_struct = json.load(f)
    questions_list = statement_struct['questions']
start=timeit.default_timer()
for question in tqdm(questions_list[0:2]):
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

