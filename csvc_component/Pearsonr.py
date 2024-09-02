# -*- encoding = utf-8 -*-
# @Time : 2022/7/8 23:01
# @Author : 高猛
# @File : Pearsonr.py
# @Software : PyCharm

import numpy as np
from scipy.stats import pearsonr
import time


class Pearsonr:
    def __init__(self, args):
        self.Index = None
        self.args = args
        self.x_dim = args.x_dim

    def fit(self, data_x_, data_y_, t):
        if t > 3:
            data_x = np.array(data_x_)
            data_y = np.array(data_y_)

            self.Index = []
            p_list = []
            for i in range(self.x_dim):
                x_list = np.array(data_x)[:, i]
                p_list.append(np.abs(pearsonr(x_list, data_y)[0]))

            if t < self.x_dim:
                self.Index.append(np.argmax(p_list))
            else:
                sort_index_ = np.argsort(p_list)
                p_interval = [p_list[sort_index_[i + 1]] - p_list[sort_index_[i]] for i in range(len(p_list) - 1)]
                self.Index += list(sort_index_[np.argmax(p_interval) + 1:])
        else:
            self.Index = []

    def get_key_variable(self):
        return self.Index
