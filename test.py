import json
from process import ProcessInterface
import params as P
import numpy as np
import yaml

func_type = ['clothing', 'turn_round', 'group_person', 'multi_entry']
param_keys = {'clothing': [],
              'turn_round': ['turnround_times', 'turnround_sense'],
              'group_person': ['groupperson_max'],
              'multi_entry': ['multientry_frequency']}
clothes = {0:'hat', 1:'sunglasses', 2:'mask'}

def set_atm_default_params():
    params = {}
    for func, param in param_keys.items():
        params[func] = {}
        for _p in param:
            params[func][_p] = getattr(P, _p)
    return params


f = open('test.json')
model_results = json.load(f)
# params = set_atm_default_params()
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
