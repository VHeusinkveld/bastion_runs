import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import processing_functions as pf

from mayavi import mlab
#%%
exp_name = "027_averages_angles_new"
res_dir = "results"
sub_dir = "average"
#%%
exp_name = "028_averages_powers_new"
res_dir = "results"
sub_dir = "power"
#%%
exp_name = "029_rotation"
res_dir = "results"
sub_dir = "power"
#%%

try_names = ["0" + str(item)+ "/" for item in [1]]

for i, try_name in enumerate(try_names):
    data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])   
    equifield_data = np.loadtxt(data_path_root + "equifield")
    n = int(np.power(len(equifield_data), 1/3)) + 1
    equifield_data = np.swapaxes(np.reshape(equifield_data, (n, n, n)), 1, 2)
    equifield_data = equifield_data*273/9.81

x = np.linspace(0, 100, n)
y = np.linspace(0, 100, n)
z = np.linspace(0, 100, n)

X, Y, Z = np.meshgrid(x, y, z)
steps = 100/(n+1)
M = np.mgrid[steps/2:100-steps/2:steps, steps/2:100-steps/2:steps, steps/2:100-steps/2:steps]

original_field = (0.2 + 9.81/1004)*Y
equifield_data = equifield_data[:,:,:] - original_field.T

hist, bin_edges = np.histogram(equifield_data, bins=50)
plt.plot(bin_edges[:-1], hist)
plt.ylim([0, 50])
plt.show()   

s = equifield_data

src = mlab.pipeline.scalar_field(M[0], M[1], M[2], s)
#mlab.pipeline.iso_surface(src, contours=[-0.1   , ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.max()*0.2, ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.max()*0.4, ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.max()*0.6, ],)
mlab.orientation_axes()
mlab.colorbar()
mlab.show()
    

"""
for j in range(n):
    plt.imshow(equifield_data[:,:,j].T - original_field, origin="lower")
    plt.colorbar()
    plt.show()
    plt.pause(0)
"""