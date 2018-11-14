import numpy as np
import matplotlib.pyplot as plt 

inversion = 0.1
g = 9.81
Tref = 273
y = np.linspace(0,100,1001);
T = 5*np.log10((y**(1/2))+1)

plt.plot(T, y)
plt.ylim([0,50])
