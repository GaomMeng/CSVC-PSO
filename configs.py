# -*- coding: UTF-8 -*-
# @Date    :2023/4/18 22:25
# @Author  :高猛
# @Project :DTPs 
# @File    :configs.py
# @IDE     :PyCharm
import argparse


def set_param():
    parser = argparse.ArgumentParser()

    ''' mpb args '''
    parser.add_argument('--s_dim', default=2, type=int)
    parser.add_argument('--x_dim', default=10, type=int)
    parser.add_argument('--x_bound', default=5., type=float)
    parser.add_argument('--peak_num', default=1, type=int)
    parser.add_argument('--peak_h', default=50, type=int)
    parser.add_argument('--peak_w', default=5, type=int)
    parser.add_argument('--peak_sigma', default=5, type=float)
    parser.add_argument('--time_fac', default=100., type=float)
    parser.add_argument('--max_step', default=100, type=float)
    parser.add_argument('--bt_type', default='linear', type=str,  help="'linear', 'sin', 'cir'")

    ''' pso args '''
    parser.add_argument('--Population_size', default=100, type=int)
    parser.add_argument('--Iteration_number', default=100, type=int)
    parser.add_argument('--Inertia_weight', default=0.75, type=float)
    parser.add_argument('--Individual_learning_factor', default=1.4, type=float)
    parser.add_argument('--Social_learning_factor', default=1.4, type=float)
    parser.add_argument('--Max_vel', default=0.8, type=float)

    ''' model args '''
    parser.add_argument('--if_crossing', default=True, type=bool)
    parser.add_argument('--if_detection', default=True, type=bool)
    parser.add_argument('--mode', default='csvc', type=str)
    parser.add_argument('--delta', default=0.9, type=float)
    parser.add_argument('--svm_kernel', default='linear', type=str,  help="'linear', 'poly', 'rbf', 'sigmoid'")

    ''' train args '''
    parser.add_argument('--rand_seed', default=10086, type=float)
    parser.add_argument('--MPB_seed', default=123, type=float)
    parser.add_argument('--filename',  default='data_save/run_data', type=str)
    parser.add_argument('--sample_num', default=20, type=int)
    parser.add_argument('--b_list', default=[10, 50, 100], type=list)
    parser.add_argument('--using_multiprocessing', default=True, type=bool)

    args = parser.parse_args()
    return args

