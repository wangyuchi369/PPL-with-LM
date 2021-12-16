import random
import json


groundtruth_file = 'annotations.json'
output_file = 'pploutput.json'
with open(output_file,'r') as f:
    output_list = json.load(f)['questions']
with open(groundtruth_file, 'r') as f:
    groundtruth_list = json.load(f)['annotations']
for i in range(len(output_list)):
    if 'ppl_top100_answers' not in output_list[i]:
        print('出问题了',i)
compare = zip(groundtruth_list,output_list)
print('共有',len(groundtruth_list))
count =0
for each_item in compare:
    groundtruth,output = each_item
    assert groundtruth['question_id']==output['question_id'] # 确保是同一问题
    if 'ppl_top100_answers' not in output:
        print('出问题了',output)
    if groundtruth['multiple_choice_answer'] in output['ppl_top100_answers']:
        count+=1
    # groundtruth_answer_list = groundtruth['answers']
    # answers_list = [i['answer'] for i in groundtruth_answer_list]
    # output_list = output['ppl_top100_answers'][0:100]
    # if len(set(answers_list).intersection(set(output_list))):
    #     count+=1
    #     print(count)
print(count/len(groundtruth_list))





# with open('forsee.json','w') as f:
#     json.dump(groundtruth,f,indent =2)
