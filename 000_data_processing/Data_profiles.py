import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from os import listdir

def one2two(data):
    data_points = int(np.sqrt(len(data)))
    return np.reshape(np.array(data),(data_points, data_points))        

#%%
data_path = "../005_MPI_compat/results/single00/profiles"
data_files = listdir(data_path)
legend = []
for file in data_files:
    time =  float(file[file.find("t=")+2:])
    if (time%20==0):
        legend.append(file)
        data = pd.read_csv(data_path+"/"+file, "\t")
        plt.plot(30*data['bdiff'], data['y'])
        print(data)
#b_ref = 0.5*data['y']*9.81/273;
#plt.plot(b_ref, data['y'])
#plt.xlim([0.25, 0.55])
plt.xlim([-0.2, 0.2])
plt.ylim([10, 35])
plt.legend(legend)
plt.show()

#%%
from matplotlib import animation
data_path = "../005_MPI_compat/results/single00/slices"
data_files = listdir(data_path)
files_length = len(data_files)

# animation function
def animate(i): 
    file = data_files[i]
    time =  float(file[file.find("t=")+2:])

    data = pd.read_csv(data_path+"/"+file, "\s")
    plt.clf()
    img = plt.contourf(one2two(data['#']), one2two(data['2:y']), one2two(data['3:z']))
    plt.colorbar()
    plt.title(file)
    
    return img

fig = plt.figure()
Nt = files_length
anim = animation.FuncAnimation(fig, animate, frames=Nt)

anim.save('animation.mp4', fps=1)

'''
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.contour(one2two(data['#']), one2two(data['2:y']), one2two(data['3:z']))
plt.show()
'''