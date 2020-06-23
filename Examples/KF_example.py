import numpy as np
import math

import clean_KF as Kalman

from numpy.random import randn
import matplotlib.pyplot as plt


def compute_data(z_var, process_var, count=1, dt=1.):
    x, vel = 0., 1.
    z_std = math.sqrt(z_var)
    p_std = math.sqrt(process_var)
    xs, zs = [], []
    for _ in range(count):
        v = vel + (randn() * p_std)
        x += v*dt
        xs.append(x)
        zs.append(x + randn() * z_std)
    return np.array(xs), np.array(zs)


real, zedd = compute_data(2.45, 4.45, 50)

xs, cv = Kalman.run_kf(data=zedd, dim_of_measurements=1, measured_var=(10,4.5), covar=(500,49), process_model=((1, 1), (0, 1)), white_noise_var=.35, dt=1, sensor_covar=5, measurement_function=(1,0))

print(xs[:,0])
plt.plot(range(1, len(zedd)+1), xs[:, 0], c ='r', label='Filter')
plt.plot(range(1, len(zedd)+1), real, c='blue', label='Real')
plt.plot(range(1, len(zedd)+1), zedd, c='orange', label='Measurements')
plt.title('Kalman Filter 2D')
plt.legend(loc=4)
plt.show()
