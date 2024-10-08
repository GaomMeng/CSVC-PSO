import math
import itertools
import random
import numpy as np
import configs

try:
    from collections.abc import Sequence
except:
    from collections import Sequence


def cone(individual, position, height, width):
    """The cone peak function to be used with scenario 2 and 3.

    :math:`f(\mathbf{x}) = h - w \sqrt{\sum_{i=1}^N (x_i - p_i)^2}`

    """
    value = 0.0
    for x, p in zip(individual, position):
        value += (x - p) ** 2
    return height - width * math.sqrt(value)


def sphere(individual, position, height, width):
    value = 0.0
    for x, p in zip(individual, position):
        value += (x - p) ** 2
    return height * value


def function1(individual, position, height, width):
    """The function1 peak function to be used with scenario 1.

    :math:`f(\mathbf{x}) = \\frac{h}{1 + w \sqrt{\sum_{i=1}^N (x_i - p_i)^2}}`

    """
    value = 0.0
    for x, p in zip(individual, position):
        value += (x - p) ** 2
    return height / (1 + width * value)


class MovingPeaks:
    """The Moving Peaks Benchmark is a fitness function changing over time. It
    consists of a number of peaks, changing in height, width and location. The
    peaks function is given by *pfunc*, which is either a function object or a
    list of function objects (the default is :func:`function1`). The number of
    peaks is determined by *npeaks* (which defaults to 5). This parameter can
    be either a integer or a sequence. If it is set to an integer the number
    of peaks won't change, while if set to a sequence of 3 elements, the
    number of peaks will fluctuate between the first and third element of that
    sequence, the second element is the initial number of peaks. When
    fluctuating the number of peaks, the parameter *number_severity* must be
    included, it represents the number of peak fraction that is allowed to
    change. The dimensionality of the search domain is *dim*. A basis function
    *bfunc* can also be given to act as static landscape (the default is no
    basis function). The argument *random* serves to grant an independent
    random number generator to the moving peaks so that the evolution is not
    influenced by number drawn by this object (the default uses random
    functions from the Python module :mod:`random`). Various other keyword
    parameters listed in the table below are required to setup the benchmark,
    default parameters are based on scenario 1 of this benchmark.

    =================== ============================= =================== =================== ======================================================================================================================
    Parameter           :data:`SCENARIO_1` (Default)  :data:`SCENARIO_2`  :data:`SCENARIO_3`    Details
    =================== ============================= =================== =================== ======================================================================================================================
    ``pfunc``           :func:`function1`             :func:`cone`        :func:`cone`        The peak function or a list of peak function.
    ``npeaks``          5                             10                  50                  Number of peaks. If an integer, the number of peaks won't change, if a sequence it will fluctuate [min, current, max].
    ``bfunc``           :obj:`None`                   :obj:`None`         ``lambda x: 10``    Basis static function.
    ``min_coord``       0.0                           0.0                 0.0                 Minimum coordinate for the centre of the peaks.
    ``max_coord``       100.0                         100.0               100.0               Maximum coordinate for the centre of the peaks.
    ``min_height``      30.0                          30.0                30.0                Minimum height of the peaks.
    ``max_height``      70.0                          70.0                70.0                Maximum height of the peaks.
    ``uniform_height``  50.0                          50.0                0                   Starting height for all peaks, if ``uniform_height <= 0`` the initial height is set randomly for each peak.
    ``min_width``       0.0001                        1.0                 1.0                 Minimum width of the peaks.
    ``max_width``       0.2                           12.0                12.0                Maximum width of the peaks
    ``uniform_width``   0.1                           0                   0                   Starting width for all peaks, if ``uniform_width <= 0`` the initial width is set randomly for each peak.
    ``lambda_``         0.0                           0.5                 0.5                 Correlation between changes.
    ``move_severity``   1.0                           1.5                 1.0                 The distance a single peak moves when peaks change.
    ``height_severity`` 7.0                           7.0                 1.0                 The standard deviation of the change made to the height of a peak when peaks change.
    ``width_severity``  0.01                          1.0                 0.5                 The standard deviation of the change made to the width of a peak when peaks change.
    ``period``          5000                          5000                1000                Period between two changes.
    =================== ============================= =================== =================== ======================================================================================================================

    Dictionaries :data:`SCENARIO_1`, :data:`SCENARIO_2` and
    :data:`SCENARIO_3` of this module define the defaults for these
    parameters. The scenario 3 requires a constant basis function
    which can be given as a lambda function ``lambda x: constant``.

    The following shows an example of scenario 1 with non uniform heights and
    widths.

    .. plot:: code/benchmarks/movingsc1.py
       :width: 67 %
    """

    def __init__(self, dim, random=random, **kargs):
        # Scenario 1 is the default
        sc = SCENARIO_4.copy()
        sc.update(kargs)

        pfunc = sc.get("pfunc")
        npeaks = sc.get("npeaks")

        random.seed(sc.get("args").rand_seed)
        self.random = random

        self.dim = dim

        self.minpeaks, self.maxpeaks = None, None
        if hasattr(npeaks, "__getitem__"):
            self.minpeaks, npeaks, self.maxpeaks = npeaks
            self.number_severity = sc.get("number_severity")

        try:
            if len(pfunc) == npeaks:
                self.peaks_function = pfunc
            else:
                self.peaks_function = self.random.sample(pfunc, npeaks)
            self.pfunc_pool = tuple(pfunc)
        except TypeError:
            self.peaks_function = list(itertools.repeat(pfunc, npeaks))
            self.pfunc_pool = (pfunc,)

        self.basis_function = sc.get("bfunc")

        self.min_coord = sc.get("min_coord")
        self.max_coord = sc.get("max_coord")

        self.min_height = sc.get("min_height")
        self.max_height = sc.get("max_height")
        uniform_height = sc.get("uniform_height")

        self.min_width = sc.get("min_width")
        self.max_width = sc.get("max_width")
        uniform_width = sc.get("uniform_width")

        self.lambda_ = sc.get("lambda_")
        self.move_severity = sc.get("move_severity")
        self.height_severity = sc.get("height_severity")
        self.width_severity = sc.get("width_severity")
        try:
            self.time_fac = sc.get("args").time_fac
        except:
            print('No time-fac!!')
            self.time_fac = 0.
        self.time_fac_sym = 0.

        self.peaks_position = [[self.random.uniform(self.min_coord, self.max_coord) for _ in range(dim)] for _ in
                               range(npeaks)]

        if uniform_height != 0:
            self.peaks_height = [uniform_height for _ in range(npeaks)]
        else:
            self.peaks_height = [self.random.uniform(self.min_height, self.max_height) for _ in range(npeaks)]

        if uniform_width != 0:
            self.peaks_width = [uniform_width for _ in range(npeaks)]
        else:
            self.peaks_width = [self.random.uniform(self.min_width, self.max_width) for _ in range(npeaks)]

        self.last_change_vector = [[self.random.random() - 0.5 for _ in range(dim)] for _ in range(npeaks)]

        self.period = sc.get("period")

        # Used by the Offline Error calculation
        self._optimum = None
        self._error = None
        self._offline_error = 0

        # Also used for auto change
        self.nevals = 0

    def globalMaximum(self):
        """Returns the global maximum value and position."""
        # The global maximum is at one peak's position
        potential_max = list()
        for func, pos, height, width in zip(self.peaks_function,
                                            self.peaks_position,
                                            self.peaks_height,
                                            self.peaks_width):
            potential_max.append((func(pos, pos, height, width), pos))
        return max(potential_max)

    def get_h(self):
        return self.peaks_height[0]

    def maximums(self):
        """Returns all visible maximums value and position sorted with the
        global maximum first.
        """
        # The maximums are at the peaks position but might be swallowed by
        # other peaks
        maximums = list()
        for func, pos, height, width in zip(self.peaks_function,
                                            self.peaks_position,
                                            self.peaks_height,
                                            self.peaks_width):
            val = func(pos, pos, height, width) + self.time_fac * self.time_fac_sym
            if val >= self.__call__(pos, count=False)[0]:
                maximums.append((val, pos))
        return sorted(maximums, reverse=True)

    def __call__(self, individual, count=False):
        """Evaluate a given *individual* with the current benchmark
        configuration.

        :param indidivudal: The individual to evaluate.
        :param count: Whether or not to count this evaluation in
                      the total evaluation count. (Defaults to
                      :data:`True`)
        """
        possible_values = []

        for func, pos, height, width in zip(self.peaks_function,
                                            self.peaks_position,
                                            self.peaks_height,
                                            self.peaks_width):
            possible_values.append(func(individual, pos, height, width))

        if self.basis_function:
            possible_values.append(self.basis_function(individual))

        fitness = max(possible_values) + self.time_fac * self.time_fac_sym

        if count:
            # Compute the offline error
            self.nevals += 1
            if self._optimum is None:
                self._optimum = self.globalMaximum()[0]
                self._error = abs(fitness - self._optimum)
            self._error = min(self._error, abs(fitness - self._optimum))
            self._offline_error += self._error

            # We exhausted the number of evaluation, change peaks for the next one.
            if self.period > 0 and self.nevals % self.period == 0:
                self.changePeaks()

        return fitness,

    def test(self, individual_dict, count=False):
        """Evaluate a given *individual* with the current benchmark
        configuration.

        :param indidivudal: The individual to evaluate.
        :param count: Whether or not to count this evaluation in
                      the total evaluation count. (Defaults to
                      :data:`True`)
        """
        individual = individual_dict['x']
        possible_values = []

        for func, pos, height, width in zip(self.peaks_function,
                                            self.peaks_position,
                                            self.peaks_height,
                                            self.peaks_width):
            possible_values.append(func(individual, pos, height, width))

        if self.basis_function:
            possible_values.append(self.basis_function(individual))

        fitness = max(possible_values) + self.time_fac * self.time_fac_sym

        if count:
            # Compute the offline error
            self.nevals += 1
            if self._optimum is None:
                self._optimum = self.globalMaximum()[0]
                self._error = abs(fitness - self._optimum)
            self._error = min(self._error, abs(fitness - self._optimum))
            self._offline_error += self._error

            # We exhausted the number of evaluation, change peaks for the next one.
            if self.period > 0 and self.nevals % self.period == 0:
                self.changePeaks()

        return fitness

    def offlineError(self):
        return self._offline_error / self.nevals

    def currentError(self):
        return self._error

    def changePeaks(self, individual=None):
        """Order the peaks to change position, height, width and number."""
        # Change the number of peaks
        if self.minpeaks is not None and self.maxpeaks is not None:
            npeaks = len(self.peaks_function)
            u = self.random.random()
            r = self.maxpeaks - self.minpeaks
            if u < 0.5:
                # Remove n peaks or less depending on the minimum number of peaks
                u = self.random.random()
                n = min(npeaks - self.minpeaks, int(round(r * u * self.number_severity)))
                for i in range(n):
                    idx = self.random.randrange(len(self.peaks_function))
                    self.peaks_function.pop(idx)
                    self.peaks_position.pop(idx)
                    self.peaks_height.pop(idx)
                    self.peaks_width.pop(idx)
                    self.last_change_vector.pop(idx)
            else:
                # Add n peaks or less depending on the maximum number of peaks
                u = self.random.random()
                n = min(self.maxpeaks - npeaks, int(round(r * u * self.number_severity)))
                for i in range(n):
                    self.peaks_function.append(self.random.choice(self.pfunc_pool))
                    self.peaks_position.append(
                        [self.random.uniform(self.min_coord, self.max_coord) for _ in range(self.dim)])
                    self.peaks_height.append(self.random.uniform(self.min_height, self.max_height))
                    self.peaks_width.append(self.random.uniform(self.min_width, self.max_width))
                    self.last_change_vector.append([self.random.random() - 0.5 for _ in range(self.dim)])

        for i in range(len(self.peaks_function)):
            # Change peak position
            shift = [self.random.random() - 0.5 for _ in range(len(self.peaks_position[i]))]
            shift_length = sum(s ** 2 for s in shift)
            shift_length = self.move_severity / math.sqrt(shift_length) if shift_length > 0 else 0

            shift = [shift_length * (1.0 - self.lambda_) * s
                     + self.lambda_ * c for s, c in zip(shift, self.last_change_vector[i])]

            shift_length = sum(s ** 2 for s in shift)
            shift_length = self.move_severity / math.sqrt(shift_length) if shift_length > 0 else 0

            shift = [s * shift_length for s in shift]

            new_position = []
            final_shift = []
            for pp, s in zip(self.peaks_position[i], shift):
                new_coord = pp + s
                if new_coord < self.min_coord:
                    new_position.append(2.0 * self.min_coord - pp - s)
                    final_shift.append(-1.0 * s)
                elif new_coord > self.max_coord:
                    new_position.append(2.0 * self.max_coord - pp - s)
                    final_shift.append(-1.0 * s)
                else:
                    new_position.append(new_coord)
                    final_shift.append(s)

            self.peaks_position[i] = new_position
            self.last_change_vector[i] = final_shift

            # Change peak height
            change = self.random.gauss(0, 1) * self.height_severity
            new_value = change + self.peaks_height[i]
            if new_value < self.min_height:
                self.peaks_height[i] = 2.0 * self.min_height - self.peaks_height[i] - change
            elif new_value > self.max_height:
                self.peaks_height[i] = 2.0 * self.max_height - self.peaks_height[i] - change
            else:
                self.peaks_height[i] = new_value

            # Change peak width
            change = self.random.gauss(0, 1) * self.width_severity
            new_value = change + self.peaks_width[i]
            if new_value < self.min_width:
                self.peaks_width[i] = 2.0 * self.min_width - self.peaks_width[i] - change
            elif new_value > self.max_width:
                self.peaks_width[i] = 2.0 * self.max_width - self.peaks_width[i] - change
            else:
                self.peaks_width[i] = new_value

        # Change time_fac
        self.time_fac_sym = self.get_sym(individual)
        self._optimum = None

    @ classmethod
    def get_sym(cls, x):
        # bt_type', default='linear', type=str,  help="'linear', 'sin', 'cir'")
        bt_type = configs.set_param().bt_type
        if bt_type == 'linear':
            sym = 1 if x[0] >= 0. else -1
        elif bt_type == 'sin':
            sym = 1 if 2 * np.sin(0.2 * np.pi * x[0]) <= x[1] else -1
        elif bt_type == 'cir':
            sym = 1 if x[0]**2 + x[1]**2 <= 15.9 else -1
        elif bt_type == 'rect':
            sym = 1 if -3.54 <= x[0] <= 3.54 and -3.54 <= x[1] <= 3.54 else -1
        else:
            print("bt_type error! ensure your bt_type: 'linear', 'sin', 'cir', 'rect'")
            raise

        return sym



SCENARIO_1 = {"pfunc": function1,
              "npeaks": 5,
              "bfunc": None,
              "min_coord": 0.0,
              "max_coord": 100.0,
              "min_height": 30.0,
              "max_height": 70.0,
              "uniform_height": 50.0,
              "min_width": 0.0001,
              "max_width": 0.2,
              "uniform_width": 0.1,
              "lambda_": 0.0,
              "move_severity": 1.0,
              "height_severity": 7.0,
              "width_severity": 0.01,
              "period": 5000}

SCENARIO_2 = {"pfunc": cone,
              "npeaks": 10,
              "bfunc": None,
              "min_coord": 0.0,
              "max_coord": 100.0,
              "min_height": 30.0,
              "max_height": 70.0,
              "uniform_height": 50.0,
              "min_width": 1.0,
              "max_width": 12.0,
              "uniform_width": 0,
              "lambda_": 0.5,
              "move_severity": 1.0,
              "height_severity": 7.0,
              "width_severity": 1.0,
              "period": 5000}

SCENARIO_3 = {"pfunc": cone,
              "npeaks": 50,
              "bfunc": lambda x: 10,
              "min_coord": 0.0,
              "max_coord": 100.0,
              "min_height": 30.0,
              "max_height": 70.0,
              "uniform_height": 0,
              "min_width": 1.0,
              "max_width": 12.0,
              "uniform_width": 0,
              "lambda_": 0.5,
              "move_severity": 1.0,
              "height_severity": 1.0,
              "width_severity": 0.5,
              "period": 1000}

SCENARIO_4 = {"pfunc": cone,
              "npeaks": 1,
              "bfunc": None,
              "min_coord": -5.,
              "max_coord": 5.0,
              "min_height": 30.0,
              "max_height": 70.0,
              "uniform_height": 50.0,
              "min_width": 1.0,
              "max_width": 12.0,
              "uniform_width": 5,
              "lambda_": 0.5,
              "move_severity": 7.0,
              "height_severity": 7.0,
              "width_severity": 1.0,
              "period": 5000,
              "time_fac": 100}


def diversity(population):
    nind = len(population)
    ndim = len(population[0])
    d = [0.0] * ndim
    for x in population:
        d = [di + xi for di, xi in zip(d, x)]
    d = [di / nind for di in d]
    return math.sqrt(sum((di - xi) ** 2 for x in population for di, xi in zip(d, x)))


# if __name__ == "__main__":
#     rnd = random.Random()
#     rnd.seed(1254)
#     mpb = MovingPeaks(dim=10, number_severity=0.1, random=rnd)
#     res = mpb([0., 0.])
#     print(f'res : {res}   type : {type(res[0])} ')
#
#     for i in range(100):
#         m = mpb.maximums()[0]
#         print(f' {i}  ::  max_fit:{round(m[0], 2)}   x1_pos : {round(m[1][0], 2)} ')
#         mpb.changePeaks([0., 0.])

