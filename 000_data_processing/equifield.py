import numpy as np
import pandas as pd
import csv
import matplotlib.pyplot as plt
import processing_functions as pf

from mayavi import mlab

binfile = True

#%%
exp_name = "027_averages_angles_new"
res_dir = "results"
sub_dir = "average"
L0 = 100
#%%
exp_name = "028_averages_powers_new"
res_dir = "results"
sub_dir = "power"
L0 = 100
#%%
## Wrong scaling ...
exp_name = "031_rotaion_2"
res_dir = "results"
sub_dir = "rotation"
L0 = 200
#%%
## Very high min res, no scaling problems
exp_name = "032_rotation_3"
res_dir = "results"
sub_dir = "rotation"
L0 = 200
#%%
## One less minres as 32 --> more speed 
exp_name = "033_rotation_4"
res_dir = "results"
sub_dir = "rotation"
L0 = 200
#%%
exp_name = "034_rotation_5"
res_dir = "results"
sub_dir = "rotation"
L0 = 200
#%%
exp_name = "035_angles_P1"
res_dir = "results"
sub_dir = "angles"
L0 = 200
#%%
exp_name = "036_anlges_P2"
res_dir = "results"
sub_dir = "angles"
L0 = 200
#%%
exp_name = "038_anlges_P2_strat4"
res_dir = "results"
sub_dir = "angles"
L0 = 200
#%%


try_names = ["0" + str(item)+ "/" for item in [6]]
fig = plt.figure(figsize=[10, 5])
legend = []

for i, try_name in enumerate(try_names):
    data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])  
    data_path_equifield = pf.data_dir([exp_name, res_dir, sub_dir+try_name + "equifields"])  
    case_data_path = data_path_root + "case"
       
    case = pd.read_csv(case_data_path, "\t")
    
    data_file = data_path_equifield + "equifield" + "t=00300"
    if binfile:
        equifield_data = np.fromfile(data_file, dtype=float, count=-1, sep='') 
    else:
        equifield_data = np.loadtxt(data_file)
    
    n = int(np.power(len(equifield_data), 1/3)) + 1
    equifield_data = np.swapaxes(np.reshape(equifield_data, (n, n, n)), 1, 2)
    equifield_data = equifield_data*273/9.81

    x = np.linspace(0.5*L0/(n+1), L0-0.5*L0/(n+1), n)
    y = np.linspace(0.5*L0/(n+1), L0-0.5*L0/(n+1), n)
    z = np.linspace(0.5*L0/(n+1), L0-0.5*L0/(n+1), n)
    
    X, Y, Z = np.meshgrid(x, y, z)
    steps = L0/(n+1)
    M = np.mgrid[steps/2:L0-steps/2:steps, steps/2:L0-steps/2:steps, steps/2:L0-steps/2:steps]
    
    original_field = (0.2 + 9.81/1004)*Y
    equifield_data = equifield_data[:,:,:] - original_field.T
    
    hist, bin_edges = np.histogram(equifield_data, bins=20)
    contractx = (0.4*4*np.cos(case["theta"].values[0]-np.pi/2))/(0.4*4*np.cos(case["theta"].values[0]-np.pi/2) + 0.4*18*(abs(np.sin(case["theta"].values[0]-np.pi/2))))
    if case["theta"].values[0]-np.pi/2 < 0 and contractx != 1:
        contractx = -1*contractx 
    contracty = 1 #np.power(case["P"].values[0], -1)
    plt.plot(contractx*(bin_edges[:-1]), contracty*hist)
    legend.append(["angle=" + str(np.round(180*case["theta"].values[0]/np.pi - 90, 1)), "cf=" + str(np.round(contractx,  2))])
#plt.xlim(left=0)
plt.ylim([0, 20])
plt.legend(legend)
plt.ylabel("log(nr) in bin")
plt.xlabel("dT [K]")
plt.show()   


     #%%
s = equifield_data

src = mlab.pipeline.scalar_field(M[0], M[1], M[2], s)
mlab.pipeline.iso_surface(src, contours=[-0.1   , ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.min()*0.2, ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.min()*0.4, ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.min()*0.6, ], opacity=0.3)
mlab.pipeline.iso_surface(src, contours=[s.max()*0.2, ], opacity=0.3)
mlab.axes()
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
#%%
start = 80
end = 120

starti = int(128/200*start)
endi = int(128/200*end)


hoi = np.average(np.average(equifield_data[starti:endi, starti:endi, :], axis=0), axis=0)
plt.plot(0.2*z+hoi, z)
plt.plot(0.2*100, 100, 'x')



