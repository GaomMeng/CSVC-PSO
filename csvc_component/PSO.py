# -*- encoding = utf-8 -*-
# @Time : 2022/6/28 17:39
# @Author : 高猛
# @File : PSO.py
# @Software : PyCharm

import numpy as np
import random
import copy


class Particle:
    # 初始化
    def __init__(self, x_max, max_vel, dim, config):

        # np.random.seed(int(str(time.time() % 10)[-6:]))
        # time.sleep(0.001)
        self.__pos = list(np.random.uniform(-x_max, x_max, dim))  # 粒子的位置
        self.__vel = list(np.random.uniform(-max_vel, max_vel, dim))  # 粒子的速度

        self.__bestPos = [0.0 for _ in range(dim)]  # 粒子最好的位置
        self.config = config
        self.config['x'] = self.__pos
        self.plm = self.config['plm']
        self.__fitnessValue = self.plm.test(self.config)  # 适应度函数值

    def set_pos(self, i, value):
        self.__pos[i] = value

    def get_pos(self):
        return self.__pos

    def set_best_pos(self, i, value):
        self.__bestPos[i] = value

    def get_best_pos(self):
        return self.__bestPos

    def set_vel(self, i, value):
        self.__vel[i] = value

    def get_vel(self):
        return self.__vel

    def set_fitness_value(self, value):
        self.__fitnessValue = value

    def get_fitness_value(self):
        return self.__fitnessValue


class PSO:
    def __init__(self, args, config):
        self.config = config
        # self.seed = np.random.seed(args.rand_seed)
        self.C1 = args.Individual_learning_factor
        self.C2 = args.Social_learning_factor
        self.W = args.Inertia_weight
        self.dim = args.x_dim  # 粒子的维度
        self.size = args.Population_size  # 粒子个数
        self.iter_num = args.Iteration_number  # 迭代次数
        self.x_max = args.x_bound
        self.max_vel = args.Max_vel  # 粒子最大速度
        self.best_fitness_value = self.config['best_fitness_value'] if 'best_fitness_value' in self.config.keys() else float('-Inf')
        self.best_position = [0.0 for i in range(self.dim)]  # 种群最优位置
        self.fitness_val_list = []  # 每次迭代最优适应值
        self.plm = self.config['plm']

        # 对种群进行初始化
        self.Particle_list = [Particle(self.x_max, self.max_vel, self.dim, self.config) for i in range(self.size)]

    def set_bestFitnessValue(self, value):
        self.best_fitness_value = value

    def get_bestFitnessValue(self):
        return self.best_fitness_value

    def set_bestPosition(self, i, value):
        self.best_position[i] = value

    def get_bestPosition(self):
        return self.best_position

    # 更新速度
    def update_vel(self, part):
        for i in range(self.dim):
            vel_value = self.W * part.get_vel()[i] + self.C1 * random.random() * (part.get_best_pos()[i] - part.get_pos()[i]) \
                        + self.C2 * random.random() * (self.get_bestPosition()[i] - part.get_pos()[i])
            if vel_value > self.max_vel:
                vel_value = self.max_vel
            elif vel_value < -self.max_vel:
                vel_value = -self.max_vel
            part.set_vel(i, vel_value)

    # 更新位置
    def update_pos(self, part):
        for i in range(self.dim):
            pos_value = part.get_pos()[i] + part.get_vel()[i]
            part.set_pos(i, pos_value)
        self.config['x'] = part.get_pos()
        value = self.plm.test(self.config)
        if value > part.get_fitness_value():
            part.set_fitness_value(value)
            for i in range(self.dim):
                part.set_best_pos(i, part.get_pos()[i])
        if value > self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            for i in range(self.dim):
                self.set_bestPosition(i, part.get_pos()[i])

    def update(self):
        pop = []
        x_list = []
        fit_list = []
        for i in range(self.iter_num):
            for part in self.Particle_list:
                self.update_vel(part)  # 更新速度
                self.update_pos(part)  # 更新位置
                pop.append([copy.deepcopy(part.get_pos()), copy.deepcopy(part.get_fitness_value())])
                x_list.append(copy.deepcopy(part.get_pos()))
                fit_list.append(copy.deepcopy(part.get_fitness_value()))

        return_dict = {'state': [np.min(fit_list), np.max(fit_list) - np.min(fit_list)],
                       'pop': pop,
                       'x_list': x_list,
                       'fit_list': fit_list,
                       'best_x': self.get_bestPosition(),
                       'best_v': self.get_bestFitnessValue()}
        return return_dict

