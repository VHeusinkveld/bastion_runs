import numpy as np
import pandas as pd

import processing_functions as pf
import data_fitting as df

import matplotlib.pyplot as plt

from os import listdir

     
def arr(data):
    return np.array(data)

try_names = ["0" + str(item)+ "/" for item in [0]]

fig1 = plt.figure("Kin Energy", figsize=[16,10], dpi=72)
fig2 = plt.figure("B Energy", figsize=[16,10], dpi=72)
fig3 = plt.figure("PB ratio", figsize=[16,10], dpi=72)
pf.plot_markup()

legend = []

for try_name in try_names :
    data_path_root = pf.data_dir(["013_multi_run", "results", "resolutions"+try_name])
    data_path = data_path_root
    data_files = listdir(data_path)
    
    case = pd.read_csv(data_path + "case", "\t")
    data = pd.read_csv(data_path + "output", "\t")
    
    legend.append(str(np.round(case["eps"].values/7.65*100, 0)[0]) + "\%")
    
    plt.figure("Kin Energy")
    plt.plot(data['t'], data['Ekin'])
    plt.xlabel(r'T [s]')
    plt.ylabel(r'$\textrm{E}_{kin}$ [J]')
    plt.legend(legend)
    plt.tight_layout()
    
    plt.figure("B Energy")
    plt.plot(data['t'], data['bE'])
    plt.xlabel(r'T [s]')
    plt.ylabel(r'$\textrm{E}_{b}$ [J]')
    plt.legend(legend)
    plt.tight_layout()    

    plt.figure("PB ratio")
    plt.plot(data['t'], (-data['bE']), 'x')
    
    x_fit, y_fit, stats = df.fit_exp(data['t'], ((-data['bE'])), 
                                     ([0.1, 0],[2, 10]), "exp")
    plt.plot(x_fit, y_fit, '--')
    
    plt.xlabel(r'T [s]')
    plt.ylabel(r'$\textrm{E}_{b}$ [J]')
    plt.xlim([0,90])
    #plt.ylim([0,1])
    plt.legend(legend)
    plt.tight_layout()
    
  

    
plt.figure("Kin Energy")    
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "Kin_energy.png")
plt.figure("B Energy")
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "B_energy.png")
plt.figure("PB ratio")
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "PB_ratio.png")
