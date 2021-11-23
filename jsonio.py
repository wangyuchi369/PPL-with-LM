import json
import random

def ppl(answer,statement):
    # TODO 根据模型得出ppl
    return random.random()

answer_file = 'a.json'
statement_file = 'b.json'
with open(answer_file,'r') as f:
    answer_list = json.load(f).values()
with open(statement_file, 'r') as f:
    statementFile = json.load(f)
    questions_list = statementFile['questions']
for question in questions_list:
    question.pop('vilt_top100_answers')
    statement = question['statement']
    res = dict()
    for each_answer in answer_list:
        res[each_answer] = ppl(each_answer,statement)
    sort = sorted(res.items(),key=lambda x:x[1], reverse=True)[0:10]
    question['answer'] = [answer[0] for answer in sort ]
with open('c.json','w') as f:
    json.dump(statementFile,f,indent =2)






