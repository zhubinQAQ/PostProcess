class Clothing():
    def __init__(self):
        self.classes = ['hat', 'sunglasses', 'mask']
        self.state = {'hat': 0, 'sunglasses': 0, 'mask': 0}

    def __call__(self, model_results):
        return model_results

    def set(self, params):
        assert isinstance(params, dict)
        if len(params):
            for k, v in params.items():
                setattr(self, k, v)
