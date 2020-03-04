import numpy as np
from PostProcess.tools.manage_state import BaseManageState


class ManageState(BaseManageState):
    def __init__(self, frame_last, max_times, noise_frame=9, pass_frame=20):
        super().__init__(frame_last)
        assert pass_frame < frame_last, 'pass frame should not be over last time'
        self.data = {}
        self.times = {}
        self.max_times = max_times
        self.noise_frame = noise_frame
        self.pass_frame = pass_frame
        self.entry_name = ''
        self.entry_time = ''
        self.signal_info = {'entry_flag': {}}

    def update(self, state):
        entry_name = state['entry_name']
        for k in self.data.keys():
            if entry_name == k:
                self.data[k].append(1)
            else:
                self.data[k].append(0)
            self.process(k)
        if entry_name not in self.data and entry_name != 'None':
            self.data[entry_name] = [1]

    def reset(self):
        self.data = []
        for k,v in self.times.items():
            self.times[k] = 0
        self.signal_info = {'entry_flag': {}}

    def smooth(self, k):
        kenel = np.array([[-1,2,5,2,-1]])
        data = np.array([self.data[k]])
        data = data.T
        flag = False
        start_ind_list = []
        stop_ind_list = []
        for i in range(self.frame_last-kenel.shape[1]):
            i_data = np.dot(kenel, data[i:i+kenel.shape[1]]) - sum(kenel.squeeze())
            if i_data == 0 and not flag:
                flag = True
                start_ind_list.append(i)
            elif i_data < 0 and flag:
                flag = False
                stop_ind_list.append(i)
        if len(stop_ind_list) < len(start_ind_list):
            stop_ind_list.append(self.frame_last-kenel.shape[1]-1)
        inds = np.array(stop_ind_list)-np.array(start_ind_list)
        inds = inds[inds > self.noise_frame]
        return inds.tolist()

    def process(self, k):
        if len(self.data[k]) < self.frame_last:
            self.signal_info['entry_flag'][k] = False
        else:
            assert len(self.data[k]) == self.frame_last
            inds = self.smooth(k)
            self.times[k] = len(inds)
            if self.times[k] >= self.max_times:
                self.signal_info['entry_flag'][k] = True
                self.entry_name += k+','
                self.entry_time += str(self.times[k])+','
            self.data[k] = self.data[k][(self.pass_frame+1):]

    def signal(self):
        info = {'entry_flag': False, 'entry_name': '', 'entry_times': 0}
        if len(self.entry_name):
            info = {'entry_flag': True,
                    'entry_name': self.entry_name,
                    'entry_times': self.entry_time}
        self.entry_name = ''
        self.entry_time = ''
        return info
