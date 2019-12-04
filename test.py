import json
from process import ProcessInterface
import params as P

func_type = ['clothing', 'turn_round', 'group_person', 'multi_entry']
param_keys = {'clothing': [],
              'turn_round': ['turnround_times', 'turnround_sense'],
              'group_person': ['groupperson_max'],
              'multi_entry': ['multientry_frequency']}


def set_atm_default_params():
    params = {}
    for func, param in param_keys.items():
        params[func] = {}
        for _p in param:
            params[func][_p] = getattr(P, _p)
    return params


f = open('test.json')
model_results = json.load(f)
print(model_results)
params = set_atm_default_params()
atm_interface = ProcessInterface(params, func_type)

for i in range(100):
    atm_result = atm_interface(model_results)
    print(atm_result)
