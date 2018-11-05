import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def data_dir(namelist):
    """
    Takes folder starting from root directory and stices them together.
    
    """
    
    for i, name in enumerate(namelist):
        if i == 0 and name[0:2] != "../":
            return_name = "../"
        elif i == 0:
            return_name = ""
            
        if name:
            return_name += name
        if name[-1] != "/":
            return_name += "/"
            
    return return_name

def one2two(data):
    """
    Converts 2D data in a 1D array to a 2D array
    """
    data_points = int(np.sqrt(len(data)))
    return np.reshape(np.array(data),(data_points, data_points))   

def plot_markup():
    font = {'family' : 'serif',
            'weight' : 'normal',
            'size'   : 38}
    mpl.rc('font', **font)
    mpl.rc('text', usetex=True)
