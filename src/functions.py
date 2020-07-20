import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats

FORMAT = '%Y%m%d_%H%M'

def nice_filename(fname, extension):
    '''
    takes filename and extension and returns nice formatted name
    '''
    return fname + '_' + datetime.now().strftime(FORMAT) + '.' + extension

def set_options(num_precision):
    '''
    sets options to what I like..
    '''
    pd.set_option('display.float_format', lambda x: '%.2f' % x)
    pd.set_option("display.precision", 3)

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print("{0} took {1:0.3f} seconds".format(method.__name__, te-ts))
        return (result, te-ts)
    return timed

def plot_data(data_df, var_to_plot, yaxis, title, xlabel, ylabel, fontsize=12):
    '''
    returns plot 
    '''
    fig, ax = plt.subplots(1, figsize=(10, 5))
    ax.bar(x = data_df[var_to_plot], height = data_df[yaxis])
    
    ax.set_title(title)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    return fig, ax