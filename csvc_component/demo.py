# -*- encoding = utf-8 -*-
# @Time : 2022/6/17 14:24
# @Author : 高猛
# @File : demo.py
# @Software : PyCharm

import csv
import math
import os

from csvc_component import MPB
import time
from tqdm import tqdm
import copy
import random
import datetime
import argparse
import numpy as np
from csvc_component.PSO import PSO
from csvc_component.CSVC_Model import CSVC_Model


def CSVC_PSO(args):
    """
    main loop of csvc-pso
    """

    '''  init environment '''
    csvc_pso = CSVC_Model(args)
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    '''  loop star '''
    progress_bar = tqdm(range(args.max_step), desc=f'ID:{args.sample_id}', total=args.max_step)
    for t in range(args.max_step):

        # choose individual by csvc-pso
        x_best = csvc_pso.choose_individual(t, mp)

        # get fitness
        fit = mp.test({'x': x_best})
        f_sum += fit

        # apply solution
        mp.changePeaks(x_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum), x_best]
            writer = csv.writer(f)
            writer.writerow(row)

        progress_bar.update()
    progress_bar.close()


def PSO_only(args):
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    for t in range(args.max_step):

        # use pso
        pso = PSO(args, {'plm': mp})
        pso_dict = pso.update()
        x_pso_best = pso_dict['best_x']

        # get fitness
        fit = mp.test({'x': x_pso_best})
        f_sum += fit
        mp.changePeaks(x_pso_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum)]
            writer = csv.writer(f)
            writer.writerow(row)


def Optimal(args):
    mp = MPB.MovingPeaks(dim=args.x_dim, npeaks=1, number_severity=0.1, args=args)
    f_sum = 0.

    for t in range(args.max_step):

        # find optimal solution
        maxinum = mp.maximums()[0]
        x_ = maxinum[1]
        bt_type = args.bt_type
        if bt_type == 'linear':
            if x_[0] >= 0:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                x_temp[0] = 0
                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'sin':
            if 2 * np.sin(0.2 * np.pi * x_[0]) <= x_[1]:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                x_temp[1] = 2 * np.sin(0.2 * np.pi * x_[0])
                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'cir':
            if x_[0]**2 + x_[1]**2 <= 15.9:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)
                sr = (15.89/(x_[0]**2 + x_[1]**2))**0.5
                x_temp[0] = x_[0] * sr
                x_temp[1] = x_[1] * sr

                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        elif bt_type == 'rect':
            if -3.54 <= x_[0] <= 3.54 and -3.54 <= x_[1] <= 3.54:
                x_best = x_
            else:
                x_temp = copy.deepcopy(x_)

                # 方形边界
                dots = [[-3.54, -3.54], [-3.54, 3.54], [3.54, -3.54], [3.54, 3.54], ]
                n = np.argmin([math.sqrt((di[0] - x_[0])**2 + (di[1] - x_[1])**2) for di in dots])
                if -3.54 <= x_[0] <= 3.54 and -3.54 <= x_[1] <= 3.54:
                    x_temp = x_
                elif -3.54 <= x_[0] <= 3.54:
                    x_temp = [dots[n][1] if xi == 1 else xd for xi, xd in enumerate(x_temp)]
                elif -3.54 <= x_[1] <= 3.54:
                    x_temp = [dots[n][0] if xi == 0 else xd for xi, xd in enumerate(x_temp)]
                else:
                    x_temp = dots[n] + x_[2:]

                if mp.test({'name': 'MP', 'x': x_}) > (mp.test({'name': 'MP', 'x': x_temp}) + 2 * args.time_fac):
                    x_best = x_
                else:
                    x_best = x_temp
        else:
            print("bt_type error! ensure your bt_type: 'linear', 'sin', 'cir', 'rect'")
            raise

        # get fitness
        fit = mp.test({'x': x_best})
        f_sum += fit
        mp.changePeaks(x_best)

        # save data
        with open(args.filename, 'a', newline='') as f:
            row = [int(t), float(fit), float(f_sum)]
            writer = csv.writer(f)
            writer.writerow(row)





