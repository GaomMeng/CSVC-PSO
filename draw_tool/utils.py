import csv
import os
import numpy as np


def get_data_list(key_list, paths, max_step):
    list_csv = list_dir(file_dir=paths)
    data_list = []
    for filename in list_csv:
        if check_key(key_list, str(filename)) and len(data_list) < 30:
            a_list = []
            with open(filename, encoding='utf-8') as f:
                reader = csv.reader(f)
                for data in list(reader)[-max_step:]:
                    if len(data) > 2:
                        a_list.append(float(data[2]))
            if len(a_list) >= max_step:
                data_list.append(a_list)
    if len(data_list) > 1:
        np_data = np.array(data_list, dtype=float)
        mean_list = []
        std_list = []
        for i in range(np_data.shape[1]):
            mean_list.append(np.mean(np_data[:, i]))
            std_list.append(np.std(np_data[:, i]) + 1e-5)
        return mean_list, std_list
    elif len(data_list) == 1:
        return data_list[0], np.zeros((len(data_list[0]), ))
    else:
        print('list error !!!')
        raise


def list_dir(file_dir):
    list_filename = []
    dir_list = os.listdir(file_dir)
    for cur_file in dir_list:
        path = os.path.join(file_dir, cur_file)
        if os.path.splitext(path)[1] == '.csv':
            csv_file = os.path.join(file_dir, cur_file)
            list_filename.append(csv_file)
        if os.path.isdir(path):
            list_dir(path)
    return list_filename


def check_key(key_list, all_list):
    for key in key_list:
        if key not in all_list:
            return False
    return True


def get_arguments(arg_list, arg_dict):
    for arg in arg_list:
        if arg in list(arg_dict.keys()):
            return arg_dict[arg]
    print(f'Missing Argument : {arg_dict[0]}')
    raise


def check_arguments(arg_list, arg_dict, default_value):
    for arg in arg_list:
        if arg in list(arg_dict.keys()):
            return arg_dict[arg]
    return default_value



