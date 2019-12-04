import numpy as np


class CountPass():
    def __init__(self, count_num=60, pass_num=50):
        self.num = []
        self.show_flag = False
        self.show_flag_old = False
        self.count_num = count_num
        self.pass_num = pass_num

    def count(self, flag):
        if flag:
            self.num.append(1)
        else:
            self.num.append(0)

    def get(self):
        if len(self.num) == self.count_num:
            num = np.array(self.num)
            if len(np.where(num == 1)[0]) > self.pass_num:
                self.show_flag = True
            else:
                self.show_flag = False
            self.num.pop(0)

    def __call__(self, flag):
        self.show_flag_old = self.show_flag
        self.count(flag)
        self.get()
        return True if ((not self.show_flag_old) and self.show_flag) else False

