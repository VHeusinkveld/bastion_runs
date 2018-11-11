import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import cm
from os import listdir

import processing_functions as pf

exp_name = "020_slices"
res_dir = "results"
sub_dir = "test"

try_names = ["0" + str(item)+ "/" for item in range(1)]

plot_dpi = 72
plot_size = [17,11] 
pf.plot_markup()

def sort_slice(e):
    return e[-3:]

      
def animate(i, k, k_old, j, slices):
    #print(i+k_old,j,k,k_old, len(data_files)) 
    file_name = data_files[i+k_old]
    #time =  float(file[file.find("t=")+2:file.find("t=")+7])
    with open(data_path+"/"+file_name) as file:
        header = file.readline().split()
        data_info = {}
        for head in header:
            place = head.find("=")
            data_info[head[0:place]] = int(head[place+1:])       
        field = file.readline()
        data = []
        for ii in range(data_info["n"]):
            line = file.readline()
            data.append([float(x) for x in line.strip().split("\t")])
        data = np.transpose(np.array(data))

        axes_data = 1*slices
        axes_data.pop(j)

        plt.clf()
        if slices[j] == "y=":
            levels = np.linspace(np.floor(-1), np.ceil(1), 21)
            data = data - data_info["y"]*(0.1+9.81/1005)
            img = plt.imshow(data, levels = levels, extent = (0,data_info["x"],0,data_info["z"]), cmap=cm.jet)
        elif slices[j] == "x=":
            img = plt.imshow(data, extent = (0,data_info["y"],0,data_info["z"]), cmap=cm.jet)
        else:
            img = plt.imshow(data, extent = (0,data_info["x"],0,data_info["y"]), cmap=cm.jet)

        plt.colorbar()
        plt.xlabel(axes_data[0][0] + " [m]")
        plt.ylabel(axes_data[1][0] + " [m]")
        plt.title(file_name)
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
                    fig = plt.figure(figsize=plot_size, dpi=plot_dpi)
                    anim = animation.FuncAnimation(fig, animate, frames=k-k_old, fargs=(k, k_old, j, slices))
                    anim.save(data_path_root + "animation_" + plane + old_depth + ".mp4", writer=writer1)        
                    plt.close()
                    k_old = 1*k 
                old_depth = file[-3:]
                
            fig = plt.figure(figsize=plot_size, dpi=plot_dpi)
            anim = animation.FuncAnimation(fig, animate, frames=k-k_old, fargs=(k, k_old, j, slices))
            anim.save(data_path_root + "animation_" + plane + cur_depth + ".mp4", writer=writer1)        
            plt.close()
            k_old = 1*k 


