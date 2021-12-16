#%%
import json
def read(output_file='annotations.json'):
    with open(output_file,'r') as f:
        output_list = json.load(f)['annotations']
        return output_list
output1 = read()[:10000]
output4 = read()[30000:40000]
output6 = read()[50000:60000]
output7 = read()[60000:70000]
output8 = read()[70000:80000]
output9 = read()[80000:90000]
output11 = read()[100000:110000]
output121 = read()[110000:114000]
output122 = read()[114000:120000]
output13 = read()[120000:130000]
output15 = read()[140000:150000]
output18 = read()[170000:180000]
output20 = read()[190000:200000]
output22 = read()[210000:]

#%%
with open('annotations.json','r') as f:
    output = json.load(f)
output['annotations'] = []
output['annotations'] = output1+output4 + output6+output7+output8+output9+output11+ output121+output122+output13+output15+output18+output20+output22
with open('annotations-part.json', 'w') as f:
    json.dump(output, f, indent =2)

