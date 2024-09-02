import shutil

from draw_tool.draw import *
from configs import set_param
from csvc_component.demo import CSVC_PSO, Optimal, PSO_only
import os
from datetime import datetime
import time
import multiprocessing as mp


def run_data():
    t_start = time.time()
    args = set_param()
    name_time = str(datetime.now().strftime("%Y-%m-%d_%H%M%S"))
    num_cores = int(mp.cpu_count())
    print("This computer has: " + str(num_cores) + " cores")
    pool = mp.Pool(num_cores - 1)

    sample_id = 0
    sampler_list = []
    for b in args.b_list:

        save_path = 'data_save/run_data'

        save_path += f'/{name_time}_{args.mode}'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        save_path += f'/data_b{int(b)}'
        if not os.path.exists(save_path):
            os.mkdir(save_path)

        if args.using_multiprocessing:
            for i in range(args.sample_num):
                rand_seed = int('1' + str(b) + str(i))
                sampler_list.append(pool.apply_async(run_one, args=(sample_id, save_path, rand_seed, b)))
                sample_id += 1
        else:
            for i in range(args.sample_num):
                rand_seed = int('1' + str(b) + str(i))
                run_one(sample_id, save_path, rand_seed, b)
                sample_id += 1

    if args.using_multiprocessing:
        # sample
        for one_sampler in sampler_list:
            one_sampler.get()

    t_all = time.time() - t_start
    print(f'\n=================================================================================\n'
          f'(using_multiprocessing == {args.using_multiprocessing})all_time is {round(t_all/3600., 2)} hours ---- {round(t_all/60., 2)} min\n'
          f'=================================================================================\n')

    return f'{name_time}_{args.mode}'


def run_one(sample_id, save_path, rand_seed, b):
    args = set_param()
    t_pso = 0
    t_max = 0
    t_svc = 0
    t_all = 0

    args.time_fac = b
    f_n = f'{save_path}/b={int(args.time_fac)}_MPB_{sample_id}_{str(datetime.now().strftime("%Y-%m-%d_%H%M%S"))}'
    args.rand_seed = rand_seed
    args.sample_id = sample_id

    t0 = time.time()
    args.filename = f_n + '_POC.csv'
    CSVC_PSO(args)

    t1 = time.time()
    args.filename = f_n + '_OPT.csv'
    Optimal(args)

    t2 = time.time()
    args.filename = f_n + '_PSO.csv'
    PSO_only(args)

    t3 = time.time()

    t_svc += float(t1 - t0)
    t_max += float(t2 - t1)
    t_pso += float(t3 - t2)
    t_all += float(t3 - t0)
    print(f'===========================================================\n'
          f'Time Costing(sample_id == {sample_id})  :    '
          f'csvc-pso: {round(t_svc, 3)}   '
          f'optimal: {round(t_max, 3)}   '
          f'pso_only: {round(t_pso, 3)}   '
          f'all time: {round(t_all, 3)}   ')
    return None


def draw_fit(filename):

    args = set_param()
    for b in args.b_list:
        save_path = f'data_save/fig_data/fig_{filename}'
        read_path = f'data_save/run_data/{filename}/data_b{int(b)}'
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        draw_from_file(f=read_path, b=int(b), save_path=f'{save_path}/MPB_b={int(b)}.png', title=filename, m=args.max_step)


if __name__ == '__main__':
    filename = run_data()
    # filename = '13131636_csvc'
    draw_fit(filename)










