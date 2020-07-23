from classes import data_Agg
import pandas as pd

if __name__ == '__main__':
    # read file
    data = pd.read_csv('../data/prices_CBSA_vaca_construction_pop.csv')
    # instantiate class object
    dataobj = data_Agg(data)
    #dataobj.save('blah', 'csv')
    print(dataobj.uniq_len)