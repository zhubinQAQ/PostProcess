from collections import defaultdict

from .task1.clothing_detect import Clothing
from .task2.turnround_detect import TurnRound
from .task3.groupperson_detect import GroupPerson
from .task4.multientry_detect import MultiEntry


class Solver():
    def __init__(self, params):
        self.params = params
        self.clothing = Clothing()
        self.turn_round = TurnRound()
        self.group_person = GroupPerson()
        self.multi_entry = MultiEntry()

        self.result = defaultdict()

    def _set(self, func_type=None):
        if func_type is not None:
            assert isinstance(func_type, str)
            _func = getattr(self, func_type)
            _func.set(self.params[func_type])
            return _func
        else:
            raise Exception('Wrong function type!')

    def run(self, func_type, model_results, **kwargs):
        '''
        :param model_results: some model_results from fore-end
        :param res: some params for keeping timing information
        '''
        func = self._set(func_type=func_type)
        func_result = func(model_results[func_type], **kwargs)
        assert isinstance(func_result, list), 'unknown return type!'
        self.result[func_type] = func_result

    def get_result(self, func_type):
        return self.result[func_type]

    def get_all_result(self):
        return self.result
