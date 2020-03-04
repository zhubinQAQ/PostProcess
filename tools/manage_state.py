class BaseManageState():
    def __init__(self, frame_last, **args):
        self.frame_last = frame_last

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
        pass

    def signal(self, args):
        """
        Return whether the state is beyond the boundary
        """
        pass