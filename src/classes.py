# this is where you import only things that the class needs
from functions import nice_filename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# this is overall class - 2 below will inherit from
class data(object):
    '''
    input: pandas dataframe
    '''
    def __init__(self, df, year):
        self.df = df
        self.nice_filename = nice_filename
        self.figsize = (10,8)
        # this will become useful later when we have multiple years of data
        self.year = year
    
    # get rent percent
    def get_pct(self, df_to_add):
        df_to_add['rent_pct'] = df_to_add['rent_price'] / df_to_add['house_price'] * 100
    
    # check nulls
    @property
    def nulls(self):
        '''
        returns counts of all nulls
        '''
        return self.df[self.df.isna().any(axis=1)].count()
    
    # return info for class
    def __repr__(self):
        return  f'This is a pd object from {self.year} with: {self.df.info()}'

    ## METHODS ##
    # drop nulls
    def drop(self):
        self.df.dropna(subset=['rent_price'], axis=0)

    # get corr
    def get_corr(self):
        return self.df.corr().style.background_gradient(cmap='coolwarm').set_precision(2)

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
        self.ax.set_title(f'{title} , {self.year}')
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
        self.ax = self.df.plot.scatter(x, y)
        return self.fig, self.ax

### make an unaggregated class here
class data_un_Agg(data):
    '''
    inherits from data class
    input: pandas dataframe
    '''
    def __init__(self, df, year):
        data.__init__(self, df, year)
        self._fix_formats()

    def _fix_formats(self):
        '''
        fix up some df issues
        '''
        self.df = self.df.astype({'CBSA': 'str'})
        self.df = self.df.astype({'ZIP': 'str'})
        self.df = self.df.iloc[:, [0,2,1,4,6,10,11,12,3,16,25]].copy()
        self.df = self.df.rename(columns={'LSAD': 'CBSA_type',
                    'NAME': 'CBSA_name',
                    'ZIP' : 'zip_code',
                    'State' : 'state',
                    'POPESTIMATE2019': 'pop_2019_est',
                    'Q2' : 'vacancy_pct',
                    'Total' : 'construction_19_Q2'})

    # check CBSAs
    @property
    def uniq_len(self):
        '''
        returns number of CBSAs
        '''
        return f"The number of CBSAs is: {len(self.df['CBSA'].unique())}"
    
    ## METHODS ##
    def agg_by_zip(self):
        '''
        aggregate by zip code and return new data obj
        '''
        self.agg_zip = self.df.groupby(['CBSA', 'CBSA_type', 'CBSA_name', 'zip_code', 'state']).agg(
            house_price = ('house_price', 'mean'),
            house_priceSD = ('house_price', 'std'),
            rent_price = ('rent_price', 'mean'),
            rent_priceSD = ('rent_price', 'std'),
            rent_priceN = ('rent_price', 'count'),
            pop_2019_est = ('pop_2019_est', 'mean'),
            vacancy_pct = ('vacancy_pct', 'mean'),
            construction_19_Q2 = ('construction_19_Q2', 'mean')
            ).reset_index()
        self.get_pct(self.agg_zip)
        return data(self.agg_zip, 2019)

    # agg by CBSA
    def agg_by_CBSA(self):
        self.agg_CBSA = self.df.groupby(['CBSA', 'CBSA_type', 'CBSA_name', 'state']).agg(
            house_price = ('house_price', 'mean'),
            house_priceSD = ('house_price', 'std'),
            rent_price = ('rent_price', 'mean'),
            rent_priceSD = ('rent_price', 'std'),
            zip_codes = ('zip_code', 'count'),
            pop_2019_est = ('pop_2019_est', 'mean'),
            vacancy_pct = ('vacancy_pct', 'mean'),
            construction_19_Q2 = ('construction_19_Q2', 'mean')
            ).reset_index()
        self.get_pct(self.agg_CBSA)
        return data(self.agg_CBSA, 2019)
    
    def agg_by_state(self):
        self.agg_state = self.df.groupby(['state']).agg(
            house_price = ('house_price', 'mean'),
            house_priceSD = ('house_price', 'std'),
            rent_price = ('rent_price', 'mean'),
            rent_priceSD = ('rent_price', 'std'),
            zip_codes = ('zip_code', 'count'),
            pop_2019_est = ('pop_2019_est', 'mean'),
            vacancy_pct = ('vacancy_pct', 'mean'),
            construction_19_Q2 = ('construction_19_Q2', 'mean')
            ).reset_index()
        self.get_pct(self.agg_state)
        return data(self.agg_state, 2019)

    # save as csv
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
        self.ax.set_title(f'{title} , {self.year}')
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
        self.ax = self.df.plot.scatter(x, y)
        return self.fig, self.ax
    
    # setup geopandas df
    def gpd_create(self):
        pass

    # plot map by factor (CBSA or state) and var
    def plot_map(self):
        pass

