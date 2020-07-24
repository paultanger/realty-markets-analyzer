# this is where you import only things that the class needs
from functions import nice_filename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class data_Agg(object):
    '''
    input: pandas dataframe
    '''
    def __init__(self, df, year):
        self.df = df.copy()
        self.nice_filename = nice_filename
        self.figsize = (10,8)
        ####### NOT WORKING !!!
        self.df['CBSA'] = self.df.astype({'CBSA': 'str'})
        self.df['ZIP'] = self.df.astype({'ZIP': 'str'})
        # this will become useful later when we have multiple years of data
        self.year = year

    # check nulls
    @property
    def nulls(self):
        '''
        returns counts of all nulls
        '''
        return self.df[self.df.isna().any(axis=1)].count()

    # check CBSAs
    @property
    def uniq_len(self):
        '''
        returns number of CBSAs
        '''
        return len(self.df['CBSA'].unique())
    
    # return info for class
    def __repr__(self):
        return  f'This is a pd object from {self.year} with: {self.df.info()}'

    ## METHODS ##
    # drop nulls

    # save as csv
    # or just put in here directly rather than a separate functions
    def save(self, fname, extension):
        '''
        accepts filename and extension
        saves as csv with timestamp added
        '''
        self.filename = self.nice_filename(fname, extension)
        self.df.to_csv(self.filename, index=False)
        return print(f'saved as {self.filename}')

    # make tables
    def best(self, n):
        '''
        return n best places to buy
        '''
        return n

    # save plot to file
    def save_plot(self, fname, extension):
        '''
        accepts filename and extension
        saves as fig in current dir with timestamp
        '''
        self.filename = self.nice_filename(fname, extension)
        self.fig.savefig(self.filename)
        return print(f'saved as {self.filename}')

    # make diff types of plots
    def boxplot(self, x, title):
        '''
        accepts column and title (str)
        returns boxplot object
        '''
        self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.ax = self.df.boxplot(column = x, rot=90, return_type='axes')
        self.ax.set_title(title)
        return self.fig, self.ax

    def histplot(self, x):
        '''
        accepts column
        returns histogram object
        '''
        self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.ax = self.df.hist(column = x, ax=self.ax)
        return self.fig, self.ax
    
    def scatter(self, x, y):
        '''
        accepts two cols to plot
        returns scatterplot object
        '''
        self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.ax = self.df.scatter(column = x, height=y)
        return self.fig, self.ax
    
    # setup geopandas df
    def gpd_create(self):
        pass