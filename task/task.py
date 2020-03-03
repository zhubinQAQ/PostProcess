import json


class Task():
    def __init__(self):
        self.data_path = ()
        self.state = {}

    def prepare_data(self, idx):
        data = {}
        if not hasattr(self, 'all_data_list'):
            self.all_data_list = []
            for path in self.data_path:
                with open(path) as f:
                    self.all_data_list.append(json.load(f))
        for data_list in self.all_data_list:
            pick_data = data_list[idx]
            data.update(pick_data)
        return data

    def process_data(self, data):
        pass

    def __call__(self, idx):
        data = self.prepare_data(idx)
        self.process_data(data)
        return self.state