import json


class Task():
    def __init__(self):
        self.data_path = ()
        self.state = {}

    def prepare_data(self, idx):
        data = {}
        for path in self.data_path:
            if not hasattr(self, 'all_data_list'):
                with open(path) as f:
                    self.all_data_list = json.load(f)
            pick_data = self.all_data_list[idx]
            data.update(pick_data)
        return data

    def process_data(self, data):
        pass

    def __call__(self, idx):
        data = self.prepare_data(idx)
        self.process_data(data)
        return self.state