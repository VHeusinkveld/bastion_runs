"""
This script plots the energy developments for different values of a set variable.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import processing_functions as pf

exp_name = "014_res02"
res_dir = "results"
sub_dir = "resolutions"

try_names = ["0" + str(item)+ "/" for item in range(8)]

plot_var = "err" 
plot_table = True

plotting = {
        "Ekin"  : ["Time [s]", r"$\textrm{E}_\textrm{kin}$ [J]", 0, 0, plot_var], 
        "bE"    : ["Time [s]", r"$\textrm{E}_\textrm{b}$ [J]", 0, 0, plot_var], 
        "n"     : ["Time [s]", "Girdpoints [\#]", 0, 0, plot_var], 
        "BP"    : ["Time [s]", r"$\textrm{E}_\textrm{b}$/W [-]", 0, 0, plot_var] 
        } 
        
plot_data = pd.DataFrame(data=plotting,
                         index=["xlabel", "ylabel", "xlim", "ylim", "legend"])
plot_dpi = 72
plot_size = [17,11] 
pf.plot_markup() 
legend = []

cases = pd.DataFrame()

for i, name in enumerate(plot_data.columns.values):
    fig = plt.figure(name, figsize=plot_size, dpi=plot_dpi)

    for j, try_name in enumerate(try_names) :
        data_path_root = pf.data_dir([exp_name, res_dir, sub_dir+try_name])
        data_path = data_path_root
        data_files = listdir(data_path)
        
        if i == 0:
            case = pd.read_csv(data_path + "case", "\t")
            case["err"] = case["eps"]/case["cu"]*100.
            cases = cases.append(case, ignore_index=True)
            
        data = pd.read_csv(data_path + "output", "\t")
        data["BP"] = np.abs(data["bE"]/data["Work"])
        

        if plot_data[name]["legend"]:
            legend.append(str(np.round(case[plot_data[name]["legend"]], 2)[0]))
        
        plt.figure(name)
        plt.plot(data["t"], data[name])
        plt.xlabel(plot_data[name]["xlabel"])
        plt.ylabel(plot_data[name]["ylabel"])
   
    if plot_data[name]["legend"]:
        plt.legend(legend, loc='center left', title=plot_data[name]["legend"],
                   bbox_to_anchor=(1, 0.5))
    if type(plot_data[name]["xlim"]) == list:
        plt.xlim(plot_data[name]["xlim"])
    if type(plot_data[name]["ylim"]) == list:
        plt.ylim(plot_data[name]["ylim"])    
    
    if name == "n":
        plt.yscale("log")  
        
    plt.figure(name)    
    plt.tight_layout()
    plt.savefig(pf.data_dir([exp_name, res_dir]) + "figure_" + name + ".png")
    plt.close()
if plot_table:
    np.round(cases, 2).to_html(pf.data_dir([exp_name, res_dir]) + "cases.html")
