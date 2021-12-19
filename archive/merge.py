#%%
import json
def read(output_file):
    with open(output_file,'r') as f:
        output_list = json.load(f)['questions']
        return output_list
output1 = read('output/output1.json')[:10000]
output2 = read('output/output2.json')[10000:20000]
output3 = read('output/output3.json')[20000:30000]
output4 = read('output/output4.json')[30000:40000]
output5 = read('output/output5.json')[40000:50000]
output6 = read('output/output6.json')[50000:60000]
output7 = read('output/output7.json')[60000:70000]
output8 = read('output/output8.json')[70000:80000]
output9 = read('output/output9.json')[80000:90000]
output10 = read('output/output10.json')[90000:100000]
output11 = read('output/output11.json')[100000:110000]
output121 = read('output/output12-1.json')[110000:114000]
output122 = read('output/output12-2.json')[114000:120000]
output13 = read('output/output13.json')[120000:130000]
output141 = read('output/output14-1.json')[130000:135000]
output142 = read('output/output14-2.json')[135000:140000]
output15 = read('output/output15.json')[140000:150000]
output161 = read('output/output16-1.json')[150000:155000]
output162 = read('output/output16-2.json')[155000:160000]
output171 = read('output/output17-1.json')[160000:165000]
output172 = read('output/output17-2.json')[165000:170000]
output18 = read('output/output18.json')[170000:180000]
output191 = read('output/output19-1.json')[180000:183000]
output192 = read('output/output19-2.json')[183000:185000]
output193 = read('output/output19-3.json')[185000:187500]
output194 = read('output/output19-4.json')[187500:190000]
output20 = read('output/output20.json')[190000:200000]
output211 = read('output/output21-1.json')[200000:202500]
output212 = read('output/output21-2.json')[202500:205000]
output213 = read('output/output21-3.json')[205000:206500]
output214 = read('output/output21-4.json')[206500:208000]
output215 = read('output/output21-5.json')[208000:210000]
output22 = read('output/output22.json')[210000:]

#%%
with open('output/output1.json','r') as f:
    output = json.load(f)
output['questions'] = []
output['questions'] = output1+output2+output3+output4 +output5+ output6+output7+output8+output9+output10+output11+ output121+output122+output13+output141+output142+output15+\
                      output161+ output162+output171+ output172+output18+output191+output192+ output193+output194+output20+output211+ output212+output213+ output214+output215+output22
with open('pploutput.json', 'w') as f:
    json.dump(output, f, indent =2)

