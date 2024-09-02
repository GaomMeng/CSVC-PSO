# -*- coding: UTF-8 -*-
# @Date    :2023/4/18 22:43
# @Author  :高猛
# @Project :DTPs
# @File    :buffer.py
# @IDE     :PyCharm


class buffer:
    def __init__(self):
        self.MAX_SIZE = 1e7
        self.memory = dict()  # {'t' : {'f_best', 'x_pso', 'f_next', 'x_best'}...}

    def store_data(self, t, data_dict):
        if str(t) not in self.memory.keys():
            self.memory[str(t)] = dict()
        for k, v in data_dict.items():
            self.memory[str(t)][k] = v

    def get_pre_data(self, t):
        x_list = []
        f_next = []
        for t_ in range(t):
            x_list.append(list(self.memory[str(t_)]["x_best"]))
            f_next.append(self.memory[str(t_)]["f_next"])
        return x_list, f_next











