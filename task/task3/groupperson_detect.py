from .utils.manage_state import ManageState


class GroupPerson():
    def __init__(self):
        self.manager = ManageState('group_person')
        self.groupperson_max = 3

    def set(self, params):
        assert isinstance(params, dict)
        if len(params):
            for k, v in params.items():
                setattr(self, k, v)

    def update_state(self, state_dict):
        self.manager.update(state_dict)

    def get_state(self):
        return self.manager.signal('turn_round')

    def __call__(self, model_results):
        ret = []
        person_num = len(model_results)
        state = 1 if person_num > self.groupperson_max else 0

        for per_person_result in model_results:
            person, bbox = per_person_result
            id, name = person
            ret.append([id, name, state])
            # TO DO: get the center point to calculate the distance among people
        self.update_state(dict(group_person=state))
        return ret