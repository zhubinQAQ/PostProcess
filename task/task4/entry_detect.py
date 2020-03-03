import json
import numpy as np
from PostProcess.core.priv_config import cfg_priv
from PostProcess.task.task import Task
from PostProcess.task.task4.utils.manage_state import ManageState


class Entry(Task):
    def __init__(self):
        self.frequency = cfg_priv.ENTRY.FREQUENCY
        self.data_path = cfg_priv.ENTRY.DATA_PATH

        self.state = {'entry_flag': False, 'entry_times': 0}

    def _manage_state(self, id, name):
        manager_name = 'state_manager_{}'.format(name)
        if not hasattr(self, manager_name):
            setattr(self, manager_name, ManageState(id, name))

    def update_state(self, manager, signal):
        manager.update(dict(multi_entry=signal))

    def get_state(self, manager):
        return manager.signal('multi_entry')

    def process_data(self, data):
        print(data)
        entry_times = 0
        self.state['entry_times'] = entry_times
        print('----')

    # def __call__(self, model_results):
    #     ret = []
    #     names = []
    #     for per_person_result in model_results:
    #         person = per_person_result
    #         id, name = person
    #         if name == 'None' or name == 'Person':
    #             continue
    #         names.append(name)
    #         if name not in self.names:
    #             self.names.append(name)
    #         self._manage_state(id, name)
    #
    #     for name in self.names:
    #         manager = getattr(self, 'state_manager_{}'.format(name))
    #         if name not in names:
    #             self.update_state(manager, 0)
    #         else:
    #             self.update_state(manager, 1)
    #
    #         id = manager.id
    #         name = manager.name
    #
    #         if self.get_state(manager):
    #             ret.append([id, name, manager.get_times('multi_entry')])
    #         else:
    #             ret.append([id, name, 0])
    #
    #     return ret
