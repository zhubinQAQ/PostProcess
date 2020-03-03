import yaml
import json
from PostProcess.task import Solver
from PostProcess.tools import FrameCount
from PostProcess.core.priv_config import cfg_priv, merge_priv_cfg_from_file, merge_priv_cfg_from_list, merge_priv_cfg_to_objdet_cfg


class ProcessInterface():
    '''
    define each type processing interface
    type: face_kpts, face_det, face_rec, ho_det (human occlusion)
    '''

    def __init__(self, type=None, cfg_file=None):
        self.type = ['hop', 'turn_round', 'group', 'entry'] if type is None else type
        if cfg_file is not None:
            merge_priv_cfg_from_file(cfg_file)
        self.solver = Solver()

        self.start_frame_count()
        self.process_frame_count = FrameCount('process_frame_count')

    def __call__(self, idx, frame_free=-1, type='all', start_flag=True):
        self.process_frame_count.add()
        if frame_free > 0:
            start_flag = self.process_frame_count.vibrate(frame_free)
        for func in self.type:
            if start_flag:
                getattr(self, func + '_frame').add()
                self.solver.run(func, idx)
        return self.get(type)

    def update(self, states):
        for k, v in states.items():
            getattr(self, k + '_state').update(v)

    def get(self, type):
        if type == 'all':
            return self.solver.get_all_state()
        else:
            if type in self.type:
                return self.solver.get_state(type)
            else:
                raise Exception('Wrong type!')

    def start_frame_count(self):
        for func in self.type:
            setattr(self, func + '_frame', FrameCount(func))

    def reset_frame_count(self):
        for func in self.type:
            getattr(self, func + '_frame').reset()

    def get_frame_count(self):
        return self.process_frame_count.frame


