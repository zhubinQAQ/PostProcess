from PostProcess.task import Solver
from PostProcess.tools import FrameCount
import yaml


def set_atm_default_params(cfg_root):
    return yaml.load(open(cfg_root))


class ProcessInterface():
    '''
    define each type processing interface
    type: face_kpts, face_det, face_rec, ho_det (human occlusion)
    '''

    def __init__(self, type):
        '''

        :param params: dict, key: function type
        :param type: ['clothing', 'turn_round', 'group_person', 'multi_entry']
        '''
        self.type = type
        self.cfg_root = 'PostProcess/cfgs/params.yaml'
        process_params = set_atm_default_params(self.cfg_root)
        self.solver = Solver(process_params)

        self.start_frame_count()
        self.process_frame_count = FrameCount('process_frame_count')

    def __call__(self, model_result, frame_free=-1, type='all'):
        if len(model_result):
            self.run(model_result, frame_free=frame_free)
        return self.get(type)

    def update_params(self):
        new_params = set_atm_default_params(self.cfg_root)
        self.solver.change_params(new_params)

    def run(self, model_result, frame_free, start_flag=True):
        model_result = self.distribute_results(model_result)
        self.process_frame_count.add()
        if frame_free > 0:
            start_flag = self.process_frame_count.vibrate(frame_free)
        for func in self.type:
            if start_flag:
                getattr(self, func + '_frame').add()
                self.update_params()
                self.solver.run(func, model_result)

    def distribute_results(self, model_result):
        '''
        distribute model results to each function solver
        clothing: [box,box,box] means hat, sunglasses, mask
        turn_round: [x, y, z] means three angles
        group_person: [boxes, boxes]
        multi_entry: [name]
        :param model_result:
        :return:
        '''
        new_model_result = {}
        key = self.type
        for _k in key:
            new_model_result[_k] = []
        for anno_each_person in model_result:
            new_model_result['clothing'].append(
                [[anno_each_person['tracking_id'], anno_each_person['name']], [0, 0, 0]])
            new_model_result['turn_round'].append(
                [[anno_each_person['tracking_id'], anno_each_person['name']], anno_each_person['Eulerangle']])
            new_model_result['group_person'].append(
                [[anno_each_person['tracking_id'], anno_each_person['name']], anno_each_person['bbox']])
            new_model_result['multi_entry'].append(
                [anno_each_person['tracking_id'], anno_each_person['name']])
        return new_model_result

    def update(self, states):
        for k, v in states.items():
            getattr(self, k + '_state').update(v)

    def get(self, type):
        if type == 'all':
            return self.solver.get_all_result()
        else:
            if type in self.type:
                return self.solver.get_result(type)
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
