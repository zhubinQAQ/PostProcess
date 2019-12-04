from .utils.manage_state import ManageState


class MultiEntry():
    def __init__(self):
        self.multientry_frequency = 3
        self.names = []

    def set(self, params):
        assert isinstance(params, dict)
        if len(params):
            for k, v in params.items():
                setattr(self, k, v)

    def _manage_state(self, id, name):
        manager_name = 'state_manager_{}'.format(name)
        if not hasattr(self, manager_name):
            setattr(self, manager_name, ManageState(id, name))

    def update_state(self, manager, signal):
        manager.update(dict(multi_entry=signal))

    def get_state(self, manager):
        return manager.signal('multi_entry')

    def __call__(self, model_results):
        ret = []
        names = []
        for per_person_result in model_results:
            person = per_person_result
            id, name = person
            if name == 'None' and 'Person':
                continue
            names.append(name)
            if name not in self.names:
                self.names.append(name)
            self._manage_state(id, name)

        for name in self.names:
            manager = getattr(self, 'state_manager_{}'.format(name))
            if name not in names:
                self.update_state(manager, 0)
            else:
                self.update_state(manager, 1)

            id = manager.id
            name = manager.name

            if self.get_state(manager):
                ret.append([id, name, 1])
            else:
                ret.append([id, name, 0])

        return ret
