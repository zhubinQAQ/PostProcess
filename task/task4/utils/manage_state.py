import numpy as np
from PostProcess.tools.manage_state import BaseManageState


class ManageState(BaseManageState):
    def __init__(self, id, name):
        super().__init__(name)
        self.id = id
        self.name = name
        self.threshold = 3
        self.noise_time = 2
        self.state = {}
        self.state_old = {}
        self.times = {}

    def update(self, state):
        for k, v in state.items():
            if not self.state:
                self.state[k] = 0
                self.times[k] = [0, ]
                self.times['signal'] = 0
            else:
                self.state_old[k] = self.state[k]
                if v:
                    self.state[k] = 1
                else:
                    self.state[k] = 0

            if self.state[k] and not self.state_old[k]:
                self.times[k].append(1)
            else:
                self.times[k].append(0)

    def reset(self):
        new = {}
        assert self.state
        for k, v in self.state.items():
            new[k] = 0
        self.state = new

    def get_times(self, k):
        return self.times[k]

    def signal(self, k):
        if len(self.times[k]) < 25 * self.noise_time:
            return False
        else:
            assert len(self.times[k]) == 25 * self.noise_time
            num = np.array(self.times[k])
            if len(np.where(num == 1)[0]) > 0:
                self.times['signal'] += 1
                self.times[k] = self.times[k][(np.where(num == 1)[0][-1]+1):]
            else:
                self.times[k].pop(0)
            return self.times['signal'] > self.threshold

    def change_last(self, last):
        self.last = last

    def __repr__(self):
        s = self.__class__.__name__ + "("
        s += "name={}, ".format(self.name)
        for k, v in self.state:
            s += "{}={} ;".format(k, v)
        s += ')'
        return s
