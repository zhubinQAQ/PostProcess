import numpy as np
import json
from .utils.manage_state import ManageState
from PostProcess.core.priv_config import cfg_priv
from PostProcess.task.task import Task


class TRound(Task):
    def __init__(self):
        self.times = cfg_priv.TROUND.TIMES
        self.sense = cfg_priv.TROUND.SENSE
        self.data_path = cfg_priv.TROUND.DATA_PATH

        self.state = {}

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
