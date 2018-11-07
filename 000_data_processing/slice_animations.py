import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import cm
from os import listdir

import processing_functions as pf

exp_name = "012_angles_MPI"
res_dir = "results"
sub_dir = "angles"

try_names = ["0" + str(item)+ "/" for item in range(4)]


def sort_slice(e):
    return e[-3:]

      
def animate(i, k, k_old, j, slices):
    #print(i+k_old,j,k,k_old, len(data_files)) 
    file = data_files[i+k_old]
    #time =  float(file[file.find("t=")+2:file.find("t=")+7])
    data = pd.read_csv(data_path+"/"+file, "\t")
    if slices[j] == "y=":
        factor = float(file[file.find("y=")+2:file.find("y=")+5])*(0.1+9.81/1005)
        data_y = 273/9.81*(pf.one2two(data["b"]))-factor
    else: 
        data_y = 273/9.81*pf.one2two(data["b"])
    
    
    axes_data = 1*slices
    axes_data.pop(j)
    plt.clf()
    if slices[j] == "y=":
        levels = np.linspace(np.floor(-1), np.ceil(1), 21)
        img = plt.contourf(pf.one2two(data[axes_data[0][0]]), pf.one2two(data[axes_data[1][0]]), data_y, vmax=1, vmin=-1, cmap=cm.jet, levels=levels)
    else: 
        levels = np.linspace(0, 12, 37)
        img = plt.contourf(pf.one2two(data[axes_data[0][0]]), pf.one2two(data[axes_data[1][0]]), data_y, cmap=cm.jet, levels=levels)
    plt.colorbar()
    plt.title(file)
    plt.tight_layout()
    
    return img

Writer = animation.writers['ffmpeg']
writer1 = Writer(fps=1, extra_args=['-r', '20'])

for i, try_name in enumerate(try_names):
    data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])
    data_path = data_path_root + "slices"
    files = listdir(data_path)
    
    slices = ["x=", "y=", "z="]
    for j, plane in enumerate(slices):
        data_files = [item for item in files if (item.find(plane) >= 0)]
        num_files = len(data_files)
        if num_files > 0:
            data_files.sort(key=sort_slice)
            old_depth = data_files[0][-3:]
            l = 0
            k_old = 0
            for k, file in enumerate(data_files):
                cur_depth = file[-3:]
                if cur_depth != old_depth:
                    fig = plt.figure(figsize=[8,5], dpi=72)
                    anim = animation.FuncAnimation(fig, animate, frames=k-k_old, fargs=(k, k_old, j, slices))
                    anim.save(data_path_root + "animation_" + plane + old_depth + ".mp4", writer=writer1)        
                    plt.close()
                    k_old = 1*k 
                old_depth = file[-3:]
                
            fig = plt.figure(figsize=[8,5], dpi=72)
            anim = animation.FuncAnimation(fig, animate, frames=k-k_old, fargs=(k, k_old, j, slices))
            anim.save(data_path_root + "animation_" + plane + cur_depth + ".mp4", writer=writer1)        
            plt.close()
            k_old = 1*k 


