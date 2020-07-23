# this is where you import only things that the class needs
from functions import nice_filename
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class data_Agg(object):
    '''
    input: pandas dataframe
    '''
    def __init__(self, df):
        self.df = df.copy()
        self.nice_filename = nice_filename
        self.df['CBSA'] = self.df.astype({'CBSA': 'str'})
        #self.df['ZIP'] = self.df.astype({'ZIP': 'str'})

    # setup vars for plotting - title axis label etc

    # methods

    # check nulls

    # drop nulls

    # save as csv
    # or just put in here directly rather than a separate functions
    def save(self, fname, extension):
        self.filename = self.nice_filename(fname, extension)
        return self.df.to_csv(self.filename)
        print(f'saved as {self.filename}')

    # check CBSAs
    @property
    def uniq_len(self, self.df):
        return self.df['CBSA'].unique()

    # return info for class
    def __repr__(self):
        return  f'This is a pd object with: \n {self.df.info()}'
    
    # setup geopandas df
    def gpd_create(self):
        pass

    # make diff types of plots
    def boxplot(self):
        pass
        # fig, axs = plt.subplots(1,figsize=(8,4))
        # #flip_num = np.arange(1, num_flips + 1)
        # axs.bar(x=list(self.prior.keys()), height=list(self.prior.values()), label=label)
        # #axs[0].plot(np.arange(1,num_flips+1),np.cumsum(data)/np.arange(1,num_flips+1))
        # #axs[0].axhline(.5, color = 'green', linestyle = '--')
        # #axs[0].axhline(p, color = 'green', linestyle = '--')
        # axs.set_xlabel('die', fontsize=16)
        # axs.set_ylabel('probability', fontsize=16)
        # axs.set_title(title)

    def histplot(self):
        pass

    def histplot(self):
        pass