
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