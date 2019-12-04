from task import Solver
from tools import FrameCount, ManageState


class ProcessInterface():
    '''
    define each type processing interface
    type: face_kpts, face_det, face_rec, ho_det (human occlusion)
    '''

    def __init__(self, params, type):
        '''

        :param params: dict, key: function type
        :param type: ['clothing', 'turn_round', 'group_person', 'multi_entry']
        '''
        self.type = type
        self.solver = Solver(params)

        self.start_frame_count()
        self.start_state_manage()
        self.process_frame_count = FrameCount('process_frame_count')
        self.process_main_count = FrameCount('process_main_count')

    def __call__(self, model_result, frame_free=-1, type='all'):
        self.run(model_result, frame_free=frame_free)
        return self.get(type)

    def run(self, model_result, frame_free, start_flag=True):
        model_result = self.distribute_results(model_result)
        for func in self.type:
            if frame_free > 0:
                self.process_frame_count.add()
                start_flag = self.process_frame_count.vibrate(frame_free)
            if start_flag:
                getattr(self, func + '_frame').add()
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
                [[anno_each_person['tracking_id'], anno_each_person['name']], [0, 1, 1]])
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

    def start_state_manage(self):
        for func in self.type:
            setattr(self, func + '_state', ManageState(func))

    def reset_state_manage(self):
        for func in self.type:
            getattr(self, func + '_state').reset()
