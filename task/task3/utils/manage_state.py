class ManageState():
    def __init__(self, name):
        self.name = name
        self.last = 25
        self.state = {}

    def update(self, state):
        for k, v in state.items():
            if not self.state:
                self.state[k] = 0
            else:
                if v:
                    self.state[k] += 1

    def reset(self):
        new = {}
        assert self.state
        for k, v in self.state.items():
            new[k] = 0
        self.state = new

    def get_times(self, key):
        return self.state[key]

    def signal(self, key):
        return self.state[key] > self.last

    def change_last(self, last):
        self.last = last

    def __repr__(self):
        s = self.__class__.__name__ + "("
        s += "name={}, ".format(self.name)
        for k, v in self.state:
            s += "{}={} ;".format(k, v)
        s += ')'
        return s
