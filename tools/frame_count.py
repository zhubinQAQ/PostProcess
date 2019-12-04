class FrameCount():
    def __init__(self, name):
        self.name = name
        self.frame = 0
        self.stop_frame = 0

    def add(self):
        self.frame += 1

    def reset(self):
        self.frame = 0

    def vibrate(self, num):
        if self.frame % num == 0:
            return True
        else:
            return False

    def sum(self):
        return self.frame

    def __repr__(self):
        s = self.__class__.__name__ + "("
        s += "name={}, ".format(self.name)
        s += "frame_num={})".format(self.frame)
        return s
