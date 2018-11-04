import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from os import listdir
font = {'family' : 'serif',
        'weight' : 'normal',
        'size'   : 18}

plt.rc('font', **font)


def one2two(data):
    data_points = int(np.sqrt(len(data)))
    return np.reshape(np.array(data),(data_points, data_points))        
def arr(data):
    return np.array(data)
try_names = ["0" + str(item)+ "/" for item in range(5)]

for try_name in try_names :
    exp_name = "011_angles"
    res_name = "results"
    cas_name = "angles"
    #try_name = "02/"
    
    data_path_root = "../" + exp_name +"/"+ res_name +"/"+ cas_name+try_name 
    
    #%%
    data_path = data_path_root + "profiles"
    data_files = listdir(data_path)
    legend = []
    fig = plt.figure(figsize=[8,5], dpi=72)
    for file in data_files:
        time =  float(file[file.find("t=")+2:])
        if (time%100==0 and time > 0):
            legend.append(file)
            data = pd.read_csv(data_path+"/"+file, "\t")
            plt.plot(30*data['bdiff'], data['y'])
            
    plt.xlabel('dT [K]')
    plt.ylabel('height [m]')
    plt.ylim([0, 100])
    plt.legend(legend)
    plt.tight_layout()
    plt.savefig(data_path_root + "profile_buoyancy.png")
    #%%
    
    data_path = data_path_root
    data = pd.read_csv(data_path_root + "/output", "\t")
    
    def my_fun(x):
        return x[-1] - x[0]
    
    fig = plt.figure(figsize=[8,5], dpi=72)
    plt.plot(data['t'], data['Work']-data['Work'][0])
    plt.plot(data['t'], data['Ekin'])
    plt.plot(data['t'], -data['bE'])
    plt.plot(data['t'], data['Ekin']-data['bE'])
    plt.legend(['Work', 'Ekin', 'bE', 'Total energy'])
    plt.xlabel('time [s]')
    plt.ylabel('Energy [J]')
    plt.tight_layout()
    plt.savefig(data_path_root + "energy.png")
    
    #%%
    from matplotlib import animation
    data_path = data_path_root + "slices"
    old_files = listdir(data_path)
    data_files = [item for item in old_files if (item.find('y=') >= 0)]
    files_length = len(data_files)
    
    # animation function
    def animate(i): 
        file = data_files[i]
        time =  float(file[file.find("t=")+2:file.find("t=")+7])
    
        data = pd.read_csv(data_path+"/"+file, "\t")
        plt.clf()
        img = plt.contourf(one2two(data['x']), one2two(data[' z']), one2two(data['b']), vmin=0, vmax=2)
        plt.colorbar()
        plt.title(file)
        plt.tight_layout()
        
        return img
    
    fig = plt.figure(figsize=[8,5], dpi=72)
    Nt = files_length
    anim = animation.FuncAnimation(fig, animate, frames=Nt)
    
    anim.save(data_path_root + 'animation.mp4', fps=2)
    
    '''
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.contour(one2two(data['#']), one2two(data['2:y']), one2two(data['3:z']))
    plt.show()
    '''