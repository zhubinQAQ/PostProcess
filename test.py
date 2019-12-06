import json
from process import ProcessInterface
import numpy as np
import yaml

func_type = ['clothing', 'turn_round', 'group_person', 'multi_entry']
clothes = {0:'hat', 1:'sunglasses', 2:'mask'}


f = open('test.json')
model_results = json.load(f)
params = yaml.load(open('params.yaml'))
print(params)
atm_interface = ProcessInterface(params, func_type)


for i in range(100):
    atm_result = atm_interface(model_results, frame_free=-1)
    s = ''
    for k,v in atm_result.items():
        for _v in v:
            if len(_v) == 2:
                if np.array(_v[1]).any():
                    inds = list(np.where(np.array(_v[1])!=0)[0])
                    s += _v[0][1] + ' : ' + k + ' (' +','.join([clothes[ind] for ind in inds])+')\n'
            elif len(_v) == 3:
                if _v[2]:
                    s += _v[1] + ' : ' + k + '\n'
            else:
                raise Exception('Error in print')
    print('[Frame {}]==>\n'.format(atm_interface.get_frame_count()), s)
