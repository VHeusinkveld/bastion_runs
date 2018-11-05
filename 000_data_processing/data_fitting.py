import numpy as np
from scipy.optimize import curve_fit

def func(x, a, b):
    return (x - b)/a

def fit_exp(xdata, ydata, bounds, return_as):
    
    """
    Takes linear spaced data and tries to fit it to an expnential function 
    """
       
    xdata = xdata[ydata>0]
    ydata = ydata[ydata>0]
    
    xdata = np.log(xdata)
    ydata = np.log(ydata)
    popt, pcov = curve_fit(func, xdata, ydata, bounds=(bounds))
    
    if return_as == "exp":
        x = np.exp(xdata)
        y = np.exp(func(xdata, *popt))
    else:
        x = xdata
        y = func(xdata, *popt)
    
    stats = {'popt' : popt,
             'pcov' : pcov}
    
    return x, y, stats
