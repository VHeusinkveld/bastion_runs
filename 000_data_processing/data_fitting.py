"""
Some usefull functions for data fitting.
"""

import numpy as np
from scipy.optimize import curve_fit

def func_lin(x, a, b):
    return (x - b)/a

def fit_exp(xdata, ydata, bounds, return_as):
    
    """
    Takes linear spaced data and tries to fit it to an expnential function 
    """
       
    xdata = xdata[ydata>0]
    ydata = ydata[ydata>0]
    
    xdata = np.log(xdata)
    ydata = np.log(ydata)
    popt, pcov = curve_fit(func_lin, xdata, ydata, bounds=(bounds))
    
    if return_as == "exp":
        x = np.exp(xdata)
        y = np.exp(func_lin(xdata, *popt))
    else:
        x = xdata
        y = func_lin(xdata, *popt)
    
    stats = {'popt' : popt,
             'pcov' : pcov}
    
    return x, y, stats


#plt.ylim([0,.03])
#plt.xlim([0,120])
#x_fit, y_fit, stats = df.fit_exp(data['t'], ((-data['bE'])), 
#                                 ([0.1, 0],[2, 10]), "exp")
#plt.plot(x_fit, y_fit, '--')