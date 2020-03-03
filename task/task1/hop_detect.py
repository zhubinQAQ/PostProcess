import json
from PostProcess.task.task import Task
from PostProcess.core.priv_config import cfg_priv


class Hop(Task):
    def __init__(self):
        self.classes = cfg_priv.HOP.CLASSES
        self.data_path = cfg_priv.HOP.DATA_PATH

        self.state = {'hop_flag': False, 'hat': 0, 'sunglasses': 0, 'mask': 0}

    def process_data(self, data):
        hop_flag = False
        for k, v in data['all_boxes'].items():
            if len(v) > 0 and not hop_flag:
                hop_flag = True
            self.state[k] = len(v)
        self.state['hop_flag'] = hop_flag
