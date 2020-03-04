import json
import numpy as np
from PostProcess.core.priv_config import cfg_priv
from PostProcess.tools.box import match_box, group_point
from PostProcess.task.task import Task
from PostProcess.task.task3.utils.manage_state import ManageState


class Group(Task):
    def __init__(self):
        self.manager = ManageState('group_person')
        self.max = cfg_priv.GROUP.MAX_NUM
        self.dis = cfg_priv.GROUP.MIN_DISTANCE
        self.data_path = cfg_priv.GROUP.DATA_PATH

        self.state = {'group_flag': False, 'group_num': 0}

    def process_data(self, data):
        all_faces = data['all_boxes']['face']
        all_heads = data['all_boxes']['head']
        faces = np.array(all_faces)
        heads = np.array(all_heads)
        if len(faces) and len(heads):
            merge_boxes = match_box(faces, heads)
            center = 0.5 * (np.vstack((merge_boxes[:, 0] + merge_boxes[:, 2], merge_boxes[:, 1] + merge_boxes[:, 3])))
            group_num = group_point(center)
            self.state['group_num'] = group_num
            self.state['group_flag'] = group_num >= self.max