from collections import defaultdict

from .task1.hop_detect import Hop
from .task2.turnround_detect import TRound
from .task3.group_detect import Group
from .task4.entry_detect import Entry


class Solver():
    def __init__(self):
        self.hop = Hop()
        self.turn_round = TRound()
        self.group = Group()
        self.entry = Entry()

        self.state = defaultdict()

    def init_state(self, idx):
        self.state.update({'frame_ind': idx})

    def _set(self, func_type=None):
        if func_type is not None:
            assert isinstance(func_type, str)
            _func = getattr(self, func_type)
            return _func
        else:
            raise Exception('Wrong function type!')

    def run(self, func_type, idx=0):
        '''
        :param model_results: some model_results from fore-end
        :param res: some params for keeping timing information
        '''
        func = self._set(func_type=func_type)
        func_state = func(idx)
        self.init_state(idx)
        assert isinstance(func_state, dict), 'unknown return type!'
        self.state[func_type] = func_state

    def get_state(self, func_type):
        return self.state[func_type]

    def get_all_state(self):
        return self.state
