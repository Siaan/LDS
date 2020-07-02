#! /usr/bin/env python
import numpy as np
import math
import sys
import os
import yaml
import pandas
#sys.path.append("/home/ubuntu/NeuroCAAS/LDS_algo/neurocaas_remote")
#import main.clean_KF as Kalman
import clean_KF as Kalman

def process_parameters(configname):

    configparams = yaml.load(open(configname, 'r'), Loader=yaml.FullLoader)
    try:
        dim_of_measurements = configparams["dim_of_measurements"]
        measured_var = configparams["measured_var"]
        covar = configparams["covar"]
        process_model = configparams["process_model"]
        white_noise_var = configparams["white_noise_var"]
        dt = configparams["dt"]
        sensor_covar = configparams["sensor_covar"]
        measurement_function = configparams["measurement_function"]

    except Exception as e:
        print("params not given")
        raise OSError("params not given correctly.")

    return dim_of_measurements, measured_var, covar, process_model, white_noise_var, dt, sensor_covar, measurement_function

def process_data_file(dataname):
    df = pandas.read_csv(dataname)
    zedd = np.array(df)

    return zedd

def process_output(x,p, output_loc):
    output_df = pd.DataFrame()
    output_df[x] = x
    output_df[p] = p
    output_df.to_csv(r'output_loc', index=False)
    return output_df





if __name__ == '__main__':
    print('No Errors')







