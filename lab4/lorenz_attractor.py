import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

sigma = 10
rho = 28
beta = 8 / 3
dt = 0.01
N = 5000

def lorenz_series(x0, y0, z0):
    data = np.zeros((N, 4))
    data[0] = [0, x0, y0, z0]
    for i in range(1, N):
        t, x, y, z = data[i-1]
        dx = sigma * (y - x)
        dy = x * (rho - z) - y
        dz = x * y - beta * z

        data[i, 0] = t + dt
        data[i, 1] = x + dx * dt
        data[i, 2] = y + dy * dt
        data[i, 3] = z + dz * dt
    return data

data1 = lorenz_series(1, 1, 1)
data2 = lorenz_series(1.0001, 1, 1)

fig1 = plt.figure()
ax1 = fig1.add_subplot(111, projection='3d')
ax1.plot(data1[:,1], data1[:,2], data1[:,3], label='Start (1,1,1)', lw=0.5)
ax1.set_xlabel('X')
ax1.set_ylabel('Y')
ax1.set_zlabel('Z')
ax1.set_title('Lorenz Attractor - Траєкторія 1')
ax1.legend()

fig2 = plt.figure()
ax2 = fig2.add_subplot(111, projection='3d')
ax2.plot(data2[:,1], data2[:,2], data2[:,3], color='red', label='Start (1.0001,1,1)', lw=0.5)
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Lorenz Attractor - Траєкторія 2')
ax2.legend()

plt.show()


# Що таке хаос? 

# Що таке атрактор Лоренца, чому він так називається, що він показує. 

# Що впливає на якість розрахунків в моделі передбачення погоди та як атрактор Лоренца показує проблеми з цим? 
