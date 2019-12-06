import numpy as np
from .utils.manage_state import ManageState


class TurnRound():
    def __init__(self):
        self.turnround_times = 3
        self.turnround_sense = 0.5

    def set(self, params):
        assert isinstance(params, dict)
        if len(params):
            for k, v in params.items():
                setattr(self, k, v)

    def _manage_state(self, id, name):
        manager_name = 'state_manager_{}'.format(name)
        if not hasattr(self, manager_name):
            setattr(self, manager_name, ManageState(id, name))
        return getattr(self, 'state_manager_{}'.format(name))

    def update_state(self, manager, angles):
        state_dict = {'turn_round': 0}
        x_angle, y_angle, z_angle = angles
        if abs(x_angle) > 50:
            state_dict['turn_round'] = 1
        manager.update(state_dict)

    def get_state(self, manager):
        return manager.signal('turn_round')

    def __call__(self, model_results):
        ret = []
        for per_person_result in model_results:
            person, angles = per_person_result
            id, name = person
            if angles == 'None' or name == 'Person':
                continue
            manager = self._manage_state(id, name)
            self.update_state(manager, angles)
            if self.get_state(manager):
                ret.append([id, name, 1])
            else:
                ret.append([id, name, 0])
        return ret
