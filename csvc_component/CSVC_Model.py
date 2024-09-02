# _*_ encoding = utf-8 _*_
# @Time : 2022/11/19 10:20
# @Author : 高猛
# @File : Model.py
# @Software : PyCharm

import copy
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC
from csvc_component.Pearsonr import Pearsonr
from csvc_component.buffer import *
from csvc_component.PSO import PSO
from sklearn.metrics.pairwise import pairwise_distances_argmin


class CSVC_Model:
    def __init__(self, args):
        self.args = args
        self.archive_p = None
        self.archive_h = buffer()
        self.key_variable = Pearsonr(args)
        self.positive_label = None

    def choose_individual(self, t, mp):
        """
        t: time step
        mp: moving peak

        return: decided solution
        """

        '''  Optimizer  '''
        self.archive_p = self._optimizer(t, mp)
        if t <= 5:  # when t<5, data is scare, using pso directly
            return self.archive_p['best_x']

        ''' time-linkage detection '''
        train_data, if_return = self._detection(t)
        if if_return:  # if it can't pass detection, using pso directly
            return self.archive_p['best_x']

        ''' train svc '''
        svc = self._train_svc(train_data)

        ''' decide, crossover '''
        x_dec = self._decide_crossover(t, svc)

        return x_dec

    def _optimizer(self, t, mp):
        pso = PSO(self.args, {'plm': mp})
        archive_p = pso.update()

        # save data
        self.archive_h.store_data(t - 1, {'f_next': archive_p['best_v']})
        self.archive_h.store_data(t, {'x_best': archive_p['best_x']})

        return archive_p

    def _detection(self, t):
        # get data
        x_tra, f_next = self.archive_h.get_pre_data(t - 1)
        self.key_variable.fit(np.array(x_tra), np.array(f_next), t - 1)

        # using k-means to cluster
        center_ = 2
        k_means = KMeans(init='k-means++', n_clusters=center_, n_init=10)
        km_list = np.array([[f] for f in f_next], dtype=float)
        k_means.fit(np.array(km_list))

        k_means_cluster_centers = np.sort(k_means.cluster_centers_, axis=0)
        k_means_labels = pairwise_distances_argmin(np.array(km_list), k_means_cluster_centers)

        # clustering f in two set according to label and checking which is positive set
        two_set = [[], []]

        for i in range(len(list(k_means_labels))):
            for k_ in range(center_):
                if int(k_means_labels[i]) == int(k_):
                    two_set[k_].append(f_next[i])
        self.positive_label = 0 if np.mean(two_set[0]) > np.mean(two_set[1]) else 1

        # calculate the difference index and make a judgment
        mu = [np.mean(f_next), np.mean(two_set[0]), np.mean(two_set[1])]
        sigma = [np.std(f_next), np.std(two_set[0]), np.std(two_set[1])]
        c_ang = sum([np.linalg.norm([mu[i] - mu[(i + 1) % 3], sigma[i] - sigma[(i + 1) % 3]]) for i in range(3)])
        l_vec = sum([np.linalg.norm([mu[i], sigma[i]]) for i in range(3)])
        dif_index = c_ang / l_vec

        if_return = True if dif_index < self.args.delta and self.args.if_detection else False

        return [x_tra, k_means_labels], if_return

    def _train_svc(self, train_data):
        x_tra, labels = train_data[0], train_data[1]
        kc = self.key_variable.get_key_variable()
        X_train = np.array([[xc for xi, xc in enumerate(x) if xi in kc] for x in x_tra])
        y_train = np.array(labels)

        svc = SVC(kernel=self.args.svm_kernel, gamma=0.5, coef0=0.5, C=1)
        svc.fit(X_train, y_train)
        return svc

    def _decide_crossover(self, t, svc):
        x_list = self.archive_p['x_list']
        f_list = self.archive_p['fit_list']
        kc = self.key_variable.get_key_variable()
        X_test = np.array([[xc for xi, xc in enumerate(x) if xi in kc] for x in x_list])
        svm_ch = svc.predict(X_test)

        x_choose = []
        f_choose = []
        for xi, xv in enumerate(x_list):
            if svm_ch[xi] == self.positive_label:
                x_choose.append(xv)
                f_choose.append(f_list[xi])
        x_svc_ = x_choose[int(np.argmax(f_choose))] if len(f_choose) > 1 else x_list[int(np.argmax(f_list))]
        x_pso_ = self.archive_p['best_x']

        # if crossing
        if self.args.if_crossing:
            key_index = self.key_variable.get_key_variable()
            x_dec_ = [x_svc_[ni] if ni in key_index else x_pso_[ni] for ni in range(self.args.x_dim)]
        else:
            x_dec_ = x_svc_

        # store best solution
        self.archive_h.store_data(t, {'x_best': x_dec_})

        return x_dec_
