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
    from datetime import datetime
    FORMAT = '%Y%m%d_%H%M'
    return fname + '_' + datetime.now().strftime(FORMAT) + '.' + extension

def scatter(df, x, y, title, xlab, ylab):
    from matplotlib.ticker import FuncFormatter
    fig, ax = plt.subplots(1, figsize=(8,8))
    ax.scatter(df[x], df[y])
    ax.ticklabel_format(style='plain')
    ax.get_xaxis().set_major_formatter(
        FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.get_yaxis().set_major_formatter(
        FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.set_xlabel(xlab, fontsize = 14)
    ax.set_ylabel(ylab, fontsize = 14)
    ax.set_title(title, fontsize = 16)
    return fig, ax

def plot_subgroup_hist(df, cols, title):
    '''
    returns plot with subplots for each col in cols list
    '''
    from matplotlib.ticker import FuncFormatter
    fig, axs = plt.subplots(1, 5, figsize=(12, 5))
    for idx, col in enumerate(cols):
        df.df.boxplot(col, ax= axs.flatten()[idx])
    # fix y axis for large values
    axs[0].get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    axs[3].get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
    fig.suptitle(title, fontsize = 20,  y=1.08)
    fig.tight_layout()
    return fig, axs

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