import numpy as np
import json
from .utils.manage_state import ManageState
from PostProcess.core.priv_config import cfg_priv
from PostProcess.task.task import Task
from PostProcess.tools.box import box_angles


class TRound(Task):
    def __init__(self):
        self.times = cfg_priv.TROUND.TIMES
        self.turnround_sense = cfg_priv.TROUND.TROUND_SENSE
        self.front_sense = cfg_priv.TROUND.FRONT_SENSE
        self.data_path = cfg_priv.TROUND.DATA_PATH

        frame_last = cfg_priv.TROUND.MANAGER.FRAME_LAST
        noise_frame = cfg_priv.TROUND.MANAGER.NOISE_FRAME
        pass_frame = cfg_priv.TROUND.MANAGER.PASS_FRAME

        self.state = {'turnround_flag': False, 'turnround_times': 0}
        self.manager = ManageState(frame_last=frame_last,
                                   max_times=self.times,
                                   noise_frame=noise_frame,
                                   pass_frame=pass_frame)

    def process_data(self, data):
        is_turnround = False
        if len(data):
            depositor_pos_box = data['depositor_pos_box']
            is_turnround, _ = box_angles(depositor_pos_box,
                                         turnround_sense=self.turnround_sense,
                                         front_sense=self.front_sense)
        self.state['turnround_flag'] = is_turnround

    def manage_state(self):
        self.manager.update(self.state)
        return self.manager.signal()
