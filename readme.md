# Realty Market Analyzer

## Overview

This is a project to gather data and develop an analysis of realty markets across the US for the purpose of long term investment properties. There are two major types of investment:

- investment for appreciation
- investment as a rental property

There are many housing price and appreciation prediction tools, but there isn't many (any?) that effectively assess factors to assist with the second type of investment: rental properties.

This project seeks to address that gap.

## Table of Contents

* [Background](#background)
* [Data sources](#data-sources)
* [Data cleaning and aggregation](#Data-cleaning-and-aggregation)
* [EDA and visualization](#Exploratory-Data-Analysis)
* [App development](#App-development)
* [Conclusions](#Conclusions)
* [End User and applications](#end-user-and-applications)
* [Risk management](#risk-management)
* [Future plans](#future-plans)

## Background

The concept of buying property with the intention to rent comes down to some simple math for now.  You need to be able to the pay the mortgage and all expenses with the rental income to enable positive cash flow as well as building equity from day 1.  A common rule is the "1 % rule", [best explained here](https://affordanything.com/one-percent-rule-gross-rent-multiplier/).  In essence, it is similar to a price to earnings ratio in the stock market as a filter - you want the monthly rent to be at least 1% of the purchase price.  This leads to payoff in about 8 years.  

## Data sources

In the current phase of this project, I have integrated the following data:

| Data             | Source | Year or time period available | year or time period focus | rows  | link                                                                                                          | format | key                           | filename                                      |
|------------------|--------|-------------------------------|---------------------------|-------|---------------------------------------------------------------------------------------------------------------|--------|-------------------------------|-----------------------------------------------|
| rent prices      | Zillow | 2014-2020                     | 2019                      | 3234  | https://www.zillow.com/research/data/                                                                         | csv    | zip code                      | Zip_ZORI_AllHomesPlusMultifamily_Smoothed.csv |
| home prices      | Zillow | 1996-2020                     | 2019                      | 30442 | https://www.zillow.com/research/data/                                                                         | csv    | zip code                      | Zip_zhvi_uc_sfr_tier_0.33_0.67_sm_sa_mon.csv  |
| new construction | Census | 2014-2019                     | 2019                      | 384   | https://www.census.gov/construction/bps/msaannual.html                                                        | xls    | CBSA                          | msaannual_201999.xls                          |
| rental vacancy   | Census | 2015-2020                     | 2019                      | 75    | https://www.census.gov/housing/hvs/data/rates.html                                                            | xlsx   | Metropolitan Statistical Area | tab4_msa_15_20_rvr.xlsx                       |
| population       | Census | 2010-2019                     | 2019                      | 81434 | https://www.census.gov/data/tables/time-series/demo/popest/2010s-total-metro-and-micro-statistical-areas.html | csv    | FIPS codes                    | cbsa-est2019-alldata.csv                      |

I also used these files to join the data together:
https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html

I used this file to crosswalk the zip codes to the CBSAs:
https://www.huduser.gov/portal/datasets/usps_crosswalk.html

This is the source of the shapefiles for the maps:
https://catalog.data.gov/dataset/tiger-line-shapefile-2019-nation-u-s-current-metropolitan-statistical-area-micropolitan-statist

Data that will be useful for modeling down the road as additional factors:

* Population:
https://www.census.gov/data/developers/data-sets/popest-popproj.html

* BLS unemployment:
https://download.bls.gov/pub/time.series/la/

* Economic indicators:
https://www.census.gov/programs-surveys/susb/data/tables.html

* Additional information on rent prices:
https://www.huduser.gov/portal/datasets/fmr.html

* Crime etc other factors:
https://www.huduser.gov/portal/datasets/socds.html

* Income data?

* Foreclosure data?

## Data cleaning and aggregation

For each of the five data sources, various rearrangements were needed to combine the data into one dataframe.  They are briefly highlighted here and more details are commented in the files.

### Rent and home price data

A description of the rental price data is here: https://www.zillow.com/research/methodology-zori-repeat-rent-27092/
I utilized the data by zip code, which is reported monthly, but not all zip codes and not every month.  In fact, some states did not have any rent data, these include: 'AK', 'ME', 'MT', 'ND', 'SD', 'VT', 'WV', 'WY'.  

A description of the home price data is here: https://www.zillow.com/research/zhvi-methodology-2019-highlights-26221/
I utilized the single family home median data by zip code.  Ideally I would pull more data and try to focus on the types of properties that would become rental units, possibly filtering by bedroom size etc.

I merged this together by month and took the means for 2019, in only a couple cases did I not have any rent price data for 2019.
I used the zip code to CBSA to associate a CBSA with each zip code and took the means for each CBSA, noting the SD which in some cases was high between zip codes, or in some CBSAs which included over 1,000 zip codes.  See under Population data for reasons for aggregating.

### Construction data

For the most part this was straightforward and had CBSA information, though only for the top 75 areas.

### Rental vacancy data

Sadly all of the files available in this area are poorly formatted excel files with outdated MSA region names but no CBSA codes.  I utilized the March 2020 "Principal cities of metropolitan and micropolitan statistical areas" file ("list2_2020.xls") from [here](https://www.census.gov/geographies/reference-files/time-series/demo/metro-micro/delineation-files.html) to resolve this and associate with current CBSA codes.

### Population data

While I had zip code specific price information, it would be difficult to include population data since Census doesn't use zip codes, and even though they have zip code tabulation areas, these don't list all zip codes in each area.  In addition, for the purposes of mapping, it would be easier to map CBSAs rather than zip codes.

## Exploratory Data Analysis

As I aggregated, I looked the variation in the data for the key variables in which I had the most data: rent and home prices.  Here, box plots highlight some potential outliers:

< box plots and histograms >

A summary of the data variation across zip codes:

< table of means, SD etc >

Once I had the data in one aggregated dataframe, I was able to look at relationships between the data.  Here is a scatterplot of the relationship between the prices:

< scatterplot >

I calculated the rent to price percent, as mentioned in the background this would be a key factor in investment decisions.  It does take into account potential expenses such as property tax etc.

## App development

Ideally this project will develop an app that will enable users to explore the data and filter based on their preferences.  Towards that end, the draft rent percent data was loaded into a map using Flask, Folium, and Heroku to deploy a browser based map, which is currently hosted here: https://realty-markets.herokuapp.com/.  Unfortunately because the map data is 50MB, it takes a while to load and I need to work further on optimizing it.

## Conclusions

In conclusion, I found:

* point 1
* point 2

## End User and applications

The intended end users and market will be those looking to invest in realty with data supported decision making tools.  Ideally this will be in a subscription website or app format.

## Future plans

* pull data from more years and analyze time series
* integrate more data sources mentioned above
* convert to a SQL database using APIs to pull and organize data
* test parameters like income to estimate others
* use bayesian techniques to estimate rent and price for areas in which we don't have data yet
* further develop app with time series slider and ability to map zip codes and standard deviation in data