"""
This script plots the vertical profiles for set variables. 
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import processing_functions as pf
from pandas.plotting import table
from os import listdir

exp_name = "028_averages_powers_new"
res_dir = "results"
sub_dir = "power"
     
try_names = ["0" + str(item)+ "/" for item in range(5)]

time_start = 0
time_offset = 0
time_interval = 30
time_end = 10000

plotting = {
        "bT"     : ["T [K]",     "height [m]", 0, 0, True, True],  
        "bdiffcalc" : ["dT [K]",    "height [m]", 0, 0, True, True],      
       # "u.x"   : ["u.x [m/s]", "height [m]", 0, 0, True, True], 
       # "u.y"   : ["u.y [m/s]", "height [m]", 0, 0, True, True], 
       # "u.z"   : ["u.z [m/s]", "height [m]", 0, 0, True, True]
        } 
        
plot_data = pd.DataFrame(data=plotting,
                         index=["xlabel", "ylabel", "xlim", "ylim", 
                                "legend", "table"])
plot_dpi = 72
plot_size = [17,11]
pf.plot_markup()

for i, try_name in enumerate(try_names) :
    data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])    
    profile_data_path = data_path_root + "profiles"
    case_data_path = data_path_root + "case"
       
    case = pd.read_csv(case_data_path, "\t")
    data_files = listdir(profile_data_path)
    
    for j, name in enumerate(plot_data.columns.values): 
        legend = []
        fig = plt.figure(name, figsize=plot_size, dpi=plot_dpi)

        if plot_data[name]["table"]:
                ax = fig.add_subplot(111)
                table(ax, np.round(case, 2), loc='top', rowLabels = [''])
                tab = ax.tables[0]
                tab.scale(1,2)
       
        for k, file in enumerate(data_files):
            time =  float(file[file.find("t=")+2:])
            
            if ((time+time_offset)%time_interval==0 and 
                time >= time_start and 
                time <= time_end):
                
                if plot_data[name]["legend"]:
                    legend.append(file)
                
                data = pd.read_csv(profile_data_path+"/"+file, "\t")
                
                data["bT"] = 273 + 273*(data["b"])/9.81 - 9.81/1004*data["y"]
                data["bdiffcalc"] = 273*(data["b"])/9.81 - (float(case["inversion"]) + 9.81/1004)*data["y"]
                
                plt.figure(name)    
                plt.plot(data[name], data["y"], '-o')

        plt.figure(name)         
        plt.xlabel(plot_data[name]["xlabel"])
        plt.ylabel(plot_data[name]["ylabel"])
        
        if plot_data[name]["legend"]:
            plt.legend(legend, loc='center left', bbox_to_anchor=(1, 0.5))
        if type(plot_data[name]["xlim"]) == list:
            plt.xlim(plot_data[name]["xlim"])
        if type(plot_data[name]["ylim"]) == list:
            plt.ylim(plot_data[name]["ylim"])
        
        
        plt.tight_layout()
        plt.savefig(data_path_root + "figure_" + name + ".png")
        plt.close()  


