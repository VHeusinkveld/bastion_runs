import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib import cm
from os import listdir

import processing_functions as pf

exp_name = "021_angles_averaged"
res_dir = "results"
sub_dir = "angles"

try_names = ["0" + str(item)+ "/" for item in range(1)]

plot_dpi = 72
plot_size = [17,11] 
pf.plot_markup()

for try_name in try_names:
    data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])
    data_path = data_path_root + "slices"
    
    case_data_path = data_path_root + "case"
    case = pd.read_csv(case_data_path, "\t")
    
    files = listdir(data_path)
    files = [file_name for file_name in files if file_name.find(".png") <= 0]
    
    slices = ["x=", "y=", "z="]
    
    for file_name in files:
        with open(data_path+"/"+file_name) as file:
            plane = [item for item in slices if file_name.find(item)>=0]
            
            header = (file.readline()).split()
            data_info = {}
            for head in header:
                place = head.find("=")
                data_info[head[0:place]] = int(head[place+1:])      
                
            for i in range(data_info["len"]):
                field = (file.readline()).strip()
                data = []
                for ii in range(data_info["n"]):
                    line = file.readline()
                    data.append([float(x) for x in line.strip().split("\t")])
                    
                data = 273/9.81*np.transpose(np.array(data))
                fig = plt.figure(figsize=plot_size, dpi=plot_dpi)
                
                if plane[0] == "y=":
                    levels = np.linspace(np.floor(-1), np.ceil(1), 21)
                    data = data - data_info["y"]*(0.2+9.81/1005)
                    img = plt.imshow(data, cmap=cm.jet, vmin=-1, vmax=1)
                    pltlblx = "x"
                    pltlbly = "z"
                    
                elif plane[0] == "x=":
                    data = np.transpose(data)
                    img = plt.imshow(data, cmap=cm.jet, origin='lower', vmin=0, vmax=data_info["y"]*(float(case["inversion"])+9.81/1005))
                    pltlblx = "y"
                    pltlbly = "z"
    
                else:
                    img = plt.imshow(data, cmap=cm.jet, origin='lower', vmin=0, vmax=data_info["y"]*(float(case["inversion"])+9.81/1005))
                    pltlblx = "x"
                    pltlbly = "y"

                plt.xlabel(pltlblx + " [m]")               
                plt.ylabel(pltlbly + " [m]") 
                plt.colorbar()
                plt.savefig(data_path +"/"+ file_name + field)
                plt.close()








