class BaseManageState():
    def __init__(self, name, **args):
        self.name = name

    def update(self, args):
        """
        Manager gets the state and records
        """
        pass

    def reset(self):
        """
        Reset manager state
        """
        pass

    def get_times(self, args):
        """
        Get the state
        """

    def signal(self, args):
        """
        Return whether the state is beyond the boundary
        """
