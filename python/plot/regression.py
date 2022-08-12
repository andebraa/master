"""
Crystal Aging Project

Script for doing polynomial, linear and
non-linear regression.

This project is distributed under the GNU General Public License v3.
For more information, see the LICENSE file in the top-level dictionary.
"""

import numpy as np
from scipy.optimize import curve_fit, differential_evolution, leastsq
import warnings


def poly_reg(x, y, n, bias=True):
    '''Polynomial regression,

    y_fit(x) = ax^n + bx^(n-1) + ... + yx + z
    
    Arguments:
    ----------
    
    x:      ndarray
            X-component of all points.
            
    y:      ndarray
            Y-component of all points.
            
    n:      int
            Order of fitting polynomial.

    bias:   bool
            Constant term, true or false.
    '''
   
    xb = []     # construct design matrix
    if bias:
        xb.append(np.ones(len(x)))
    for i in range(1, n+1):
        xb.append(x**i)
    xb = np.asarray(xb).T

    beta = np.linalg.inv(xb.T.dot(xb)).dot(xb.T).dot(y)
    return beta.flatten()[::-1]


def lin_reg(x, y, f):
    '''Linear regression with any function f(x),

    y_fit(x) = af(x) + b

    Arguments:
    ----------

    x:      ndarray
            X-component of all points.

    y:      ndarray
            Y-component of all points.

    f:      func
            Function to fit, has to be vectorized.
            
    '''

    xb = np.c_[np.ones((len(x), 1)), f(x)]

    beta = np.linalg.inv(xb.T.dot(xb)).dot(xb.T).dot(y)
    return beta.flatten()[::-1]


def nonlin_reg(x, y, f, bounds, seed=3, **kwargs):
    '''Non-linear regression with any function f(x),

    y_fit(x) = f(x; *params)
    '''
    # function for genetic algorithm to minimize (sum of squared error)
    def sumOfSquaredError(parameterTuple):
        warnings.filterwarnings("ignore") # do not print warnings by genetic algorithm
        val = f(x, *parameterTuple)
        return np.sum((y - val) ** 2.0)


    def generate_Initial_Parameters():
        # "seed" the numpy random number generator for repeatable results
        result = differential_evolution(sumOfSquaredError, bounds, seed=seed)
        return result.x

    # generate initial parameter values
    geneticParameters = generate_Initial_Parameters()

    # curve fit the test data
    fittedParameters, pcov = curve_fit(f, x, y, geneticParameters, **kwargs)

    print('Parameters', fittedParameters)

    modelPredictions = f(x, *fittedParameters) 

    absError = modelPredictions - y

    SE = np.square(absError) # squared errors
    MSE = np.mean(SE) # mean squared errors
    RMSE = np.sqrt(MSE) # Root Mean Squared Error, RMSE
    Rsquared = 1.0 - (np.var(absError) / np.var(y))
    print('RMSE:', RMSE)
    print('R-squared:', Rsquared)
    return fittedParameters


def multiple_reg(x, y, f, const, params0, **kwargs):
    """Do same non-linear regression on multiple curves
    """

    def leastsq_func(params, *args):
        x, y = args[:2]
        const = args[2:]
        yfit = []
        for i in range(len(x)):
            yfit = np.append(yfit, f(x[i],*const[i],*params))
        return y-yfit

    # turn const into 2d-array if 1d is given
    const = np.asarray(const)
    if len(const.shape) < 2:
        const = np.atleast_2d(const).T

    # ensure that y is flat and x is nested
    if hasattr(y[0], "__len__"):
        y = [item for sublist in y for item in sublist]
    if not hasattr(x[0], "__len__"):
        x = np.tile(x, (len(const), 1))
    x_ = [item for sublist in x for item in sublist]
    assert len(x_) == len(y)

    # collect all arguments in a tuple
    y = np.asarray(y)
    args=[x,y] + list(const)
    args=tuple(args)   #doesn't work if args is a list!!

    return leastsq(leastsq_func, params0, args=args, **kwargs)


if __name__ == "__main__":
    

    def fit(x,T,A,n,m):
        return A/(n+1.0)*np.power(T,(n+1.0))*np.power(x,m)

    # prepare dataset with some noise
    params = [0.001, 1.01, -0.8]
    Ts = [10, 50]

    x = np.linspace(10, 100, 100)
    y = np.empty((len(Ts), len(x)))
    for i in range(len(Ts)):
        y[i] = fit(x, Ts[i], *params) + np.random.uniform(0, 0.01, size=len(x))
    
    # do regression
    params0 = [0.002, 1.5, -0.5]
    opt_params, _ = multiple_reg(x, y, f=fit, const=Ts, params0=params0, maxfev=10000)
    print(opt_params)

    # plot
    import matplotlib.pyplot as plt
    for i in range(len(Ts)):
        plt.scatter(x, y[i], label=f"T={Ts[i]}")
        plt.plot(x, fit(x, Ts[i], *opt_params), '--k')
    plt.legend(loc='best')
    plt.show()



