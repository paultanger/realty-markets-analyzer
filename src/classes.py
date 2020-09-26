# this is where you import only things that the class needs
from functions import nice_filename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# this is overall class - below will inherit from
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
    
    # check nulls
    @property
    def nulls(self):
        '''
        returns counts of all nulls
        '''
        return self.df[self.df.isna().any(axis=1)].count()
    
    # check levels of factor
    def uniq(self, factor):
        '''
        returns levels of cat variable
        '''
        return f"The number of {factor} is: {self.df[factor].unique()}"

    def uniq_len(self, factor):
        '''
        returns count of levels of cat variable
        '''
        return f"The number of {factor} is: {len(self.df[factor].unique())}"
    
    # return info for class
    def __repr__(self):
        return  f'This is a pd object from {self.year} with: {self.df.info()}'

    ## METHODS ##
    # get rent percent
    def get_pct(self, df_to_add):
        df_to_add['rent_pct'] = df_to_add['rent_price'] / df_to_add['house_price'] * 100
    
    # drop nulls
    @property
    def drop(self):
        self.df.dropna(subset=['rent_price'], axis=0)

    # get corr
    def get_corr(self):
        return self.df.corr(method='spearman').style.background_gradient(cmap='coolwarm').set_precision(2)

    # just return as df
    def as_df(self):
        '''
        return back as a pandas df
        '''
        return self.df

    # save as csv
    # or just put in here directly rather than a separate functions
    def save(self, fname):
        '''
        accepts filename
        saves as csv with timestamp added
        '''
        self.filename = self.nice_filename(fname, 'csv')
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

    def histplot(self, cols, title):
        '''
        accepts column list
        returns histogram object
        '''
        from matplotlib.ticker import FuncFormatter
        self.fig, self.axs = plt.subplots(1, len(cols), figsize=self.figsize)
        for idx, col in enumerate(cols):
            self.df.boxplot(col, ax= self.axs.flatten()[idx])
        # fix y axis for large values
        self.axs[0].get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        self.axs[3].get_yaxis().set_major_formatter(FuncFormatter(lambda x, p: format(int(x), ',')))
        self.fig.suptitle(title, fontsize = 20,  y=1.08)
        return self.fig, self.axs
    
    def scatter(self, x, y, xlab, ylab, title):
        '''
        accepts two cols to plot
        returns scatterplot object
        '''
        self.fig, self.ax = plt.subplots(1, figsize=self.figsize)
        self.ax = self.df.plot.scatter(x, y)
        from matplotlib.ticker import FuncFormatter
        self.ax.ticklabel_format(style='plain')
        self.ax.get_xaxis().set_major_formatter(
            FuncFormatter(lambda x, p: format(int(x), ',')))
        self.ax.get_yaxis().set_major_formatter(
            FuncFormatter(lambda x, p: format(int(x), ',')))
        self.ax.set_xlabel(xlab, fontsize = 14)
        self.ax.set_ylabel(ylab, fontsize = 14)
        self.ax.set_title(title, fontsize = 16)
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
        self.agg_zip['rent_CV'] = self.agg_zip['rent_priceSD'] / self.agg_zip['rent_price']
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
        self.agg_CBSA['rent_CV'] = self.agg_CBSA['rent_priceSD'] / self.agg_CBSA['rent_price']
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

    # setup geopandas df
    def gpd_create(self):
        fp = '../data/tl_2019_us_state/tl_2019_us_state.shp'
        map_states = gpd.read_file(fp)
        map_states = map_states[map_states['REGION'] != '9']
        # sure there is a better way but for now.. to make the maps bigger
        map_states = map_states[map_states['STUSPS'] != 'AK']
        map_states = map_states[map_states['STUSPS'] != 'HI']
        # set the filepath and load in a shapefile
        fp = '../data/tl_2019_us_cbsa/tl_2019_us_cbsa.shp'
        map_df = gpd.read_file(fp)
        map_df['CBSAFP'] = map_df['CBSAFP'].astype(str)
        agg_CBSA_mapdf = gpd.pd.merge(map_df, agg_CBSA.df, left_on = 'CBSAFP', right_on = 'CBSA')
        agg_CBSA_mapdf = agg_CBSA_mapdf[agg_CBSA_mapdf['state'] != 'AK']
        agg_CBSA_mapdf = agg_CBSA_mapdf[agg_CBSA_mapdf['state'] != 'HI']
        return map_states, agg_CBSA_mapdf

    # plot map by factor (CBSA or state) and var
    def plot_map(self, title, col):
        '''
        returns a map fig with col of interest plotted
        '''
        self.fig, self.axs = plt.subplots(1,2, figsize=(20, 10))
        self.ax.set_aspect('equal')
        map_states.geometry.boundary.plot(color=None, alpha = .5, ax=self.axs[0], linewidth=0.3)
        map_states.geometry.boundary.plot(color=None, alpha = .5, ax=self.axs[1], linewidth=0.3)

        agg_CBSA_mapdf.plot(column='rent_pct', cmap='YlGnBu', ax=self.axs[0], linewidth = 0.8)
        agg_CBSA_mapdf.plot(column='rent_priceSD', cmap='YlGnBu', ax=self.axs[1], linewidth = 0.8)

        xlim = ([map_states.total_bounds[0],  map_states.total_bounds[2]])
        ylim = ([map_states.total_bounds[1],  map_states.total_bounds[3]])

        self.axs[0].set_xlim(xlim)
        self.axs[0].set_ylim(ylim)
        self.axs[1].set_xlim(xlim)
        self.axs[1].set_ylim(ylim)

        self.axs[0].set_title('rent percent, 2019', x=0.5, y=1.08, fontsize=14)
        self.axs[1].set_title('rent price SD, 2019', x=0.5, y=1.08, fontsize=14)
        self.axs[0].axis('off')
        self.axs[1].axis('off')
        return self.fig, self.axs

### make an unaggregated class here
class data_un_Agg_no_rent(data):
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
                    # 'Q2' : 'vacancy_pct',
                    'Total' : 'construction_19_Q2'})

    ## METHODS ##
    def agg_by_zip(self):
        '''
        aggregate by zip code and return new data obj
        '''
        self.agg_zip = self.df.groupby(['CBSA', 'CBSA_type', 'CBSA_name', 'zip_code', 'state']).agg(
            house_price = ('house_price', 'mean'),
            house_priceSD = ('house_price', 'std'),
            # rent_price = ('rent_price', 'mean'),
            # rent_priceSD = ('rent_price', 'std'),
            # rent_priceN = ('rent_price', 'count'),
            pop_2019_est = ('pop_2019_est', 'mean'),
            # vacancy_pct = ('vacancy_pct', 'mean'),
            # construction_19_Q2 = ('construction_19_Q2', 'mean')
            ).reset_index()
        # self.get_pct(self.agg_zip)
        # self.agg_zip['rent_CV'] = self.agg_zip['rent_priceSD'] / self.agg_zip['rent_price']
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
            # vacancy_pct = ('vacancy_pct', 'mean'),
            construction_19_Q2 = ('construction_19_Q2', 'mean')
            ).reset_index()
        self.get_pct(self.agg_CBSA)
        self.agg_CBSA['rent_CV'] = self.agg_CBSA['rent_priceSD'] / self.agg_CBSA['rent_price']
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

    # setup geopandas df
    def gpd_create(self):
        fp = '../data/tl_2019_us_state/tl_2019_us_state.shp'
        map_states = gpd.read_file(fp)
        map_states = map_states[map_states['REGION'] != '9']
        # sure there is a better way but for now.. to make the maps bigger
        map_states = map_states[map_states['STUSPS'] != 'AK']
        map_states = map_states[map_states['STUSPS'] != 'HI']
        # set the filepath and load in a shapefile
        fp = '../data/tl_2019_us_cbsa/tl_2019_us_cbsa.shp'
        map_df = gpd.read_file(fp)
        map_df['CBSAFP'] = map_df['CBSAFP'].astype(str)
        agg_CBSA_mapdf = gpd.pd.merge(map_df, agg_CBSA.df, left_on = 'CBSAFP', right_on = 'CBSA')
        agg_CBSA_mapdf = agg_CBSA_mapdf[agg_CBSA_mapdf['state'] != 'AK']
        agg_CBSA_mapdf = agg_CBSA_mapdf[agg_CBSA_mapdf['state'] != 'HI']
        return map_states, agg_CBSA_mapdf

    # plot map by factor (CBSA or state) and var
    def plot_map(self, title, col):
        '''
        returns a map fig with col of interest plotted
        '''
        self.fig, self.axs = plt.subplots(1,2, figsize=(20, 10))
        self.ax.set_aspect('equal')
        map_states.geometry.boundary.plot(color=None, alpha = .5, ax=self.axs[0], linewidth=0.3)
        map_states.geometry.boundary.plot(color=None, alpha = .5, ax=self.axs[1], linewidth=0.3)

        agg_CBSA_mapdf.plot(column='rent_pct', cmap='YlGnBu', ax=self.axs[0], linewidth = 0.8)
        agg_CBSA_mapdf.plot(column='rent_priceSD', cmap='YlGnBu', ax=self.axs[1], linewidth = 0.8)

        xlim = ([map_states.total_bounds[0],  map_states.total_bounds[2]])
        ylim = ([map_states.total_bounds[1],  map_states.total_bounds[3]])

        self.axs[0].set_xlim(xlim)
        self.axs[0].set_ylim(ylim)
        self.axs[1].set_xlim(xlim)
        self.axs[1].set_ylim(ylim)

        self.axs[0].set_title('rent percent, 2019', x=0.5, y=1.08, fontsize=14)
        self.axs[1].set_title('rent price SD, 2019', x=0.5, y=1.08, fontsize=14)
        self.axs[0].axis('off')
        self.axs[1].axis('off')
        return self.fig, self.axs
