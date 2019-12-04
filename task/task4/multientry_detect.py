from .utils.manage_state import ManageState


class MultiEntry():
    def __init__(self):
        self.multientry_frequency = 3

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

    def update_state(self, manager):
        manager.update(dict(multi_entry=1))

    def get_state(self, manager):
        return manager.signal('multi_entry')

    def __call__(self, model_results):
        ret = []
        for per_person_result in model_results:
            person = per_person_result
            id, name = person
            manager = self._manage_state(id, name)
            self.update_state(manager)
            if self.get_state(manager):
                ret.append([id, name, 1])
            else:
                ret.append([id, name, 0])
        return ret
