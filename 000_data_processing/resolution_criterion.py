import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import listdir
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 36}

plt.rc('font', **font)
plt.rc('text', usetex=True)

def one2two(data):
    data_points = int(np.sqrt(len(data)))
    return np.reshape(np.array(data),(data_points, data_points))        
def arr(data):
    return np.array(data)
try_names = ["0" + str(item)+ "/" for item in [1,2,3]]


fig1 = plt.figure("Kin Energy", figsize=[16,10], dpi=72)
fig2 = plt.figure("B Energy", figsize=[16,10], dpi=72)
fig3 = plt.figure("PB ratio", figsize=[16,10], dpi=72)

legend = []

for try_name in try_names :
    exp_name = "013_res"
    res_name = "results"
    cas_name = "angles"
    
    data_path_root = "../" + exp_name +"/"+ res_name +"/"+ cas_name+try_name 
    
    data_path = data_path_root
    data_files = listdir(data_path)
    
    case = pd.read_csv(data_path +"/"+ "case", "\t")
    data = pd.read_csv(data_path +"/"+ "output", "\t")
    
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
    plt.plot(data['t'], -data['Work']/data['bE'])
    plt.xlabel(r'T [s]')
    plt.ylabel(r'$\textrm{P/E}_{b}$ [J]')
    plt.legend(legend)
    plt.tight_layout()        
    
    
    
    
    
plt.figure("Kin Energy")    
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "Kin_energy.png")
plt.figure("B Energy")
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "B_energy.png")
plt.figure("PB ratio")
plt.savefig("../" + exp_name +"/"+ res_name +"/"+ "PB_ratio.png")
