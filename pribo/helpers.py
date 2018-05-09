from __future__ import print_function
from __future__ import division
import numpy as np
from datetime import datetime
from scipy.stats import norm
from scipy.optimize import minimize
import heapq as hp
from heapq import heappush, heappop


def to_int_ndarray(x):
    templist = list()
    for temp in x:
        templist.append(round(temp))
        
    return np.array(templist)
 
def better_conf(x,y):
    print("Please compare these two configuration, if (1) better than (2),please input 1.Otherwise input 2\n")
    print("(1)\n")
    print(x)
    print("(2)\n")
    print(y)
    result = input()
    if str(result) == '1':
        return x
    return y
    

def config_filter(x,y):
    """
     This function is design for prior knowledge input. You can modify this function for specify prior strategy
    """
    largest_index = hp.nlargest(10,range(len(y)),y.take)
    result = {}
    for i in range(0,10):
        result[y[largest_index[i]]] = x[largest_index[i]]
    return result
    
    
def get_lcm(x,y):
        if x > y:
           greater = x
        else:
            greater=y
        
        while(True):
           if((greater % x == 0) and (greater % y == 0)):
               lcm = greater
               break
           greater += 1
           
        return lcm
 
def do_filter(xlist):
    xlist = sorted(xlist.items())
    result = xlist[0][1]
    for i in range(len(xlist)-1,0,-1):
        if i < len(xlist) -10 and i <0:
            break
        result = better_conf(result, xlist[i][1])
        print("better config is")
        print(result)
    return result
        
    
def acq_max(ac, gp, y_max, bounds, random_state, n_warmup=100000, n_iter=250):
    """
    A function to find the maximum of the acquisition function

    It uses a combination of random sampling (cheap) and the 'L-BFGS-B'
    optimization method. First by sampling `n_warmup` (1e5) points at random,
    and then running L-BFGS-B from `n_iter` (250) random starting points.

    Parameters
    ----------
    :param ac:
        The acquisition function object that return its point-wise value.

    :param gp:
        A gaussian process fitted to the relevant data.

    :param y_max:
        The current maximum known value of the target function.

    :param bounds:
        The variables bounds to limit the search of the acq max.

    :param random_state:
        instance of np.RandomState random number generator

    :param n_warmup:
        number of times to randomly sample the aquisition function

    :param n_iter:
        number of times to run scipy.minimize

    Returns
    -------
    :return: x_max, The arg max of the acquisition function.
    """

    # Warm up with random points
    
    x_tries =  np.around(random_state.uniform(bounds[:, 0], bounds[:, 1],
                                   size=(n_warmup, bounds.shape[0])))
    ys = ac(x_tries, gp=gp, y_max=y_max)
    x_dict= config_filter(x_tries,ys)
    #x_max = x_tries[ys.argmax()]
    #max_acq = ys.max()
    #max_acq = ys[x_index]
    xitems = x_dict.items()
    #sorted(xitems)
    max_acq = sorted(xitems)[0][0]

    # Explore the parameter space more throughly
    x_seeds = np.around(random_state.uniform(bounds[:, 0], bounds[:, 1],
                                   size=(n_iter, bounds.shape[0])))
     
    for x_try in x_seeds:
        # Find the minimum of minus the acquisition function
        res = minimize(lambda x: -ac(x.reshape(1, -1), gp=gp, y_max=y_max),
                       x_try.reshape(1, -1),
                       bounds=bounds,
                       method="L-BFGS-B")
        
        # Store it if better than previous minimum(maximum).
        if max_acq is None or -res.fun[0] <= max_acq:
            #x_max = np.around(res.x)
            x_dict[-res.fun[0]] = x_try 
            max_acq = -res.fun[0]
            

    # Clip output to make sure it lies within the bounds. Due to floating
    # x_maxdict contains morethan
    x_max = do_filter(x_dict)
    print("After compare 10 configuration")
    lastResult = np.clip(x_max, bounds[:, 0], bounds[:, 1])
    print("temp Max is")
    print(lastResult)
    return lastResult


class UtilityFunction(object):
    """
    An object to compute the acquisition functions.
    """

    def __init__(self, kind, kappa, xi):
        """
        If UCB is to be used, a constant kappa is needed.
        """
        self.kappa = kappa

        self.xi = xi

        if kind not in ['ucb', 'ei', 'poi']:
            err = "The utility function " \
                  "{} has not been implemented, " \
                  "please choose one of ucb, ei, or poi.".format(kind)
            raise NotImplementedError(err)
        else:
            self.kind = kind

    def utility(self, x, gp, y_max):
        if self.kind == 'ucb':
            return self._ucb(x, gp, self.kappa)
        if self.kind == 'ei':
            return self._ei(x, gp, y_max, self.xi)
        if self.kind == 'poi':
            return self._poi(x, gp, y_max, self.xi)

    @staticmethod
    def _ucb(x, gp, kappa):
        mean, std = gp.predict(x, return_std=True)
        return mean + kappa * std

    @staticmethod
    def _ei(x, gp, y_max, xi):
        mean, std = gp.predict(x, return_std=True)
        z = (mean - y_max - xi)/std
        return (mean - y_max - xi) * norm.cdf(z) + std * norm.pdf(z)

    @staticmethod
    def _poi(x, gp, y_max, xi):
        mean, std = gp.predict(x, return_std=True)
        z = (mean - y_max - xi)/std
        return norm.cdf(z)


def unique_rows(a):
    """
    A functions to trim repeated rows that may appear when optimizing.
    This is necessary to avoid the sklearn GP object from breaking

    :param a: array to trim repeated rows from

    :return: mask of unique rows
    """
    if a.size == 0:
        return np.empty((0,))

    # Sort array and kep track of where things should go back to
    order = np.lexsort(a.T)
    reorder = np.argsort(order)

    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1)

    return ui[reorder]


def ensure_rng(random_state=None):
    """
    Creates a random number generator based on an optional seed.  This can be
    an integer or another random state for a seeded rng, or None for an
    unseeded rng.
    """
    if random_state is None:
        random_state = np.random.RandomState()
    elif isinstance(random_state, int):
        random_state = np.random.RandomState(random_state)
    else:
        assert isinstance(random_state, np.random.RandomState)
    return random_state


class BColours(object):
    BLUE = '\033[94m'
    CYAN = '\033[36m'
    GREEN = '\033[32m'
    MAGENTA = '\033[35m'
    RED = '\033[31m'
    ENDC = '\033[0m'


class PrintLog(object):

    def __init__(self, params):

        self.ymax = None
        self.xmax = None
        self.params = params
        self.ite = 1

        self.start_time = datetime.now()
        self.last_round = datetime.now()

        # sizes of parameters name and all
        self.sizes = [max(len(ps), 7) for ps in params]

        # Sorted indexes to access parameters
        self.sorti = sorted(range(len(self.params)),
                            key=self.params.__getitem__)

    def reset_timer(self):
        self.start_time = datetime.now()
        self.last_round = datetime.now()

    def print_header(self, initialization=True):

        if initialization:
            print("{}Initialization{}".format(BColours.RED,
                                              BColours.ENDC))
        else:
            print("{}Bayesian Optimization{}".format(BColours.RED,
                                                     BColours.ENDC))

        print(BColours.BLUE + "-" * (29 + sum([s + 5 for s in self.sizes])) +
            BColours.ENDC)

        print("{0:>{1}}".format("Step", 5), end=" | ")
        print("{0:>{1}}".format("Time", 6), end=" | ")
        print("{0:>{1}}".format("Value", 10), end=" | ")

        for index in self.sorti:
            print("{0:>{1}}".format(self.params[index],
                                    self.sizes[index] + 2),
                  end=" | ")
        print('')

    def print_step(self, x, y, warning=False):

        print("{:>5d}".format(self.ite), end=" | ")

        m, s = divmod((datetime.now() - self.last_round).total_seconds(), 60)
        print("{:>02d}m{:>02d}s".format(int(m), int(s)), end=" | ")

        if self.ymax is None or self.ymax < y:
            self.ymax = y
            self.xmax = x
            print("{0}{2: >10.5f}{1}".format(BColours.MAGENTA,
                                             BColours.ENDC,
                                             y),
                  end=" | ")

            for index in self.sorti:
                print("{0}{2: >{3}.{4}f}{1}".format(
                            BColours.GREEN, BColours.ENDC,
                            x[index],
                            self.sizes[index] + 2,
                            min(self.sizes[index] - 3, 6 - 2)
                        ),
                      end=" | ")
        else:
            print("{: >10.5f}".format(y), end=" | ")
            for index in self.sorti:
                print("{0: >{1}.{2}f}".format(x[index],
                                              self.sizes[index] + 2,
                                              min(self.sizes[index] - 3, 6 - 2)),
                      end=" | ")

        if warning:
            print("{}Warning: Test point chose at "
                  "random due to repeated sample.{}".format(BColours.RED,
                                                            BColours.ENDC))

        print()

        self.last_round = datetime.now()
        self.ite += 1

    def print_summary(self):
        pass

