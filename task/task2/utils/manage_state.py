import numpy as np
from PostProcess.tools.manage_state import BaseManageState


class ManageState(BaseManageState):
    def __init__(self, frame_last, max_times, noise_frame=9, pass_frame=20):
        super().__init__(frame_last)
        assert pass_frame < frame_last, 'pass frame should not be over last time'
        self.data = []
        self.times = 0
        self.max_times = max_times
        self.noise_frame = noise_frame
        self.pass_frame = pass_frame
        self.signal_info = {'turnround_flag': False, 'turnround_times': 0}

    def update(self, state):
        _data = 1 if state['turnround_flag'] else 0
        self.data.append(_data)
        self.process()

    def reset(self):
        self.data = []
        self.times = 0
        self.signal_info = {'turnround_flag': False, 'turnround_times': 0}

    def smooth(self):
        kenel = np.array([[-1,2,5,2,-1]])
        data = np.array([self.data])
        # smooth_data = np.zeros_like(data)
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

    def process(self):
        if len(self.data) < self.frame_last:
            self.signal_info['turnround_flag'] = False
        else:
            assert len(self.data) == self.frame_last
            inds = self.smooth()
            self.times = len(inds)
            self.signal_info['turnround_flag'] = self.times >= self.max_times
            self.signal_info['turnround_times'] = self.times
            self.data = self.data[(self.pass_frame+1):]

    def signal(self):
        return self.signal_info
