from classes import data_Agg
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    # read file
    data = pd.read_csv('../data/prices_CBSA_vaca_construction_pop.csv')
    # instantiate class object
    dataobj = data_Agg(data, 2019)
    #dataobj.save('blah', 'csv')
    dataobj.uniq_len
    dataobj.nulls
    #thefig, theax = dataobj.boxplot('rent_price', 'the title')
    #plt.show()
    #dataobj.save_plot('testsave', 'png')
    thefig, theax = dataobj.histplot('rent_price')
    #dataobj.save_plot('hist', 'png')
    #dataobj.scatter('rent_price', 'house_price')
    new_agg = dataobj.agg_by_zip()
