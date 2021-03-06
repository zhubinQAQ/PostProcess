import json
import numpy as np
from PostProcess.core.priv_config import cfg_priv
from PostProcess.task.task import Task
from PostProcess.tools.box import box_angles
from PostProcess.task.task4.utils.manage_state import ManageState
from PostProcess.task.task4.utils.facelib import FaceLib


class Entry(Task):
    def __init__(self):
        self.frequency = cfg_priv.ENTRY.FREQUENCY
        self.data_path = cfg_priv.ENTRY.DATA_PATH

        self.turnround_sense = cfg_priv.TROUND.TROUND_SENSE
        self.front_sense = cfg_priv.TROUND.FRONT_SENSE

        similarity_threshold = cfg_priv.FACE_RECO.SIMILARITY_THRESHOLD
        feature_path = cfg_priv.FACE_RECO.FEATURE_PATH
        self.facelib = FaceLib(threshold=similarity_threshold, path=feature_path)

        frame_last = cfg_priv.ENTRY.MANAGER.FRAME_LAST
        noise_frame = cfg_priv.ENTRY.MANAGER.NOISE_FRAME
        pass_frame = cfg_priv.ENTRY.MANAGER.PASS_FRAME

        self.state = {'entry_flag': False, 'entry_name': '', 'entry_times': 0}
        self.manager = ManageState(frame_last=frame_last,
                                   max_times=self.frequency,
                                   noise_frame=noise_frame,
                                   pass_frame=pass_frame)

    def process_data(self, data):
        entry_flag = False
        if len(data):
            depositor_pos_box = data['depositor_pos_box']
            depositor_face_feature = data['depositor_face_feature']
            _, is_front = box_angles(depositor_pos_box,
                                     turnround_sense=self.turnround_sense,
                                     front_sense=self.front_sense)
            if is_front:
                name = self.facelib(depositor_face_feature)
                self.state['entry_name'] = name
                entry_flag = name != 'None'
        self.state['entry_flag'] = entry_flag

    def manage_state(self):
        self.manager.update(self.state)
        return self.manager.signal()