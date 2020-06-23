import numpy as np
from filterpy.kalman import KalmanFilter
import matplotlib.pyplot as plt
from filterpy.common import Q_discrete_white_noise
from filterpy.stats import plot_covariance_ellipse


def preprocess(num_measured, measured_var, covar, process_model, white_noise_var, dt, sensor_covar, measurement_function, B=0, U=0):

    dim_z = num_measured
    X = np.array(measured_var)
    P = np.diag(covar)
    A = np.array(process_model)
    Q = Q_discrete_white_noise(dim=X.shape[0], dt=dt, var=white_noise_var) #dim = shape of X?
    B = B
    U = U
    R = np.array([[sensor_covar]])
    H = np.array([measurement_function])
    return (dim_z, X, P, A, Q, dt, R, H, B, U)

def create_kf_and_assign_predict_update(dim_z, X, P, A, Q, dt, R, H, B, U):
    kf = KalmanFilter(dim_x=X.shape[0], dim_z=dim_z)
    kf.x = X
    kf.P = P
    kf.F = A
    kf.Q = Q
    kf.B = B
    kf.U = U
    kf.R = R
    kf.H = H
    return kf


# data = zedd
def run_kf(data, dim_of_measurements, measured_var, covar, process_model, white_noise_var, dt, sensor_covar,
           measurement_function):
    xs, cv = [], []
    dim_z, X, P, A, Q, dt, R, H, B, U = preprocess(num_measured=dim_of_measurements, measured_var=measured_var,
                                                   covar=covar,
                                                   process_model=process_model, white_noise_var=white_noise_var, dt=dt,
                                                   sensor_covar=sensor_covar, measurement_function=measurement_function)
    kf = create_kf_and_assign_predict_update(dim_z, X, P, A, Q, dt, R, H, B, U)

    for i in data:
        kf.predict()
        kf.update(i)

        xs.append(kf.x)
        cv.append(kf.P)

    xs, cv = np.array(xs), np.array(cv)
    return xs, cv, kf

def run_smoother(kf, xs, ps):
    x, P, K, Pp = kf.rts_smoother(Xs=xs, Ps=ps)
    return x, P

def visualise(x, y, x_real, x_messy):
    plt.figure(figsize=(10,10))
    plt.plot(range(1, len(x)+1), x[:, 0], c='r', label='Smoothed data')
    plt.plot(range(1, len(x_messy) + 1), x_messy, '--o', c='g', label='Noisy Measurement')
    plt.plot(range(1, len(x_real) + 1), x_real, '--o', c='royalblue', label='True position')
    # plt.plot(range(1, len(x)+1), cv, c='r', label='Smoothed data')

    plt.legend()
    plt.title('RTS Smoother')
    plt.show()
    return




