from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd
import boto3
import s3fs

app = Flask(__name__)

@app.route('/')

def index():
    ###### ALL THIS STUFF IS CAUSING TIME OUT ERRORS - SAVE HTML AND LOAD IT FOR NOW

    # set the filepath and load in a shapefile
    #fp = '../data/tl_2019_us_cbsa/tl_2019_us_cbsa.shp'
    # for heroku
    #map_df = gpd.read_file(f'zip+s3://realty-markets-analyzer/tl_2019_us_cbsa.zip')
    #map_df = gpd.read_file(fp)
    #map_df['CBSAFP'] = map_df['CBSAFP'].astype(str)
    # for heroku
    #agg_CBSA = pd.read_csv('s3://realty-markets-analyzer/agg_CBSA.csv')
    #agg_CBSA['CBSA'] = agg_CBSA['CBSA'].astype(str)
    #agg_CBSA_mapdf = gpd.pd.merge(map_df, agg_CBSA, left_on = 'CBSAFP', right_on = 'CBSA')
    # agg_CBSA_mapdf = gpd.read_file('s3://realty-markets-analyzer/agg_CBSA_mapdf.geojson')

    # salina, KS - center of US!
    # center_coords = (38.8255662,-97.7023273)

    # # setup map
    # map1 = folium.Map(location = center_coords, zoom_start=5)

    # # setup scale
    # myscale = (agg_CBSA_mapdf['rent_pct'].quantile((0,0.1,0.75,0.9,0.98,1))).tolist()

    # # this was a great guide: https://vverde.github.io/blob/interactivechoropleth.html
    # folium.Choropleth(geo_data = agg_CBSA_mapdf, 
    #                 data = agg_CBSA_mapdf,
    #                 columns = ['CBSA', 'rent_pct'], # first is key, second is value
    #                 key_on = 'feature.properties.CBSA', # 'feature.properties.{}'.format(id_field),
    #                 fill_color = 'YlGnBu', 
    #                 fill_opacity = 0.3, 
    #                 line_opacity = 0.2,  
    #                 threshold_scale = myscale,
    #                 legend_name = 'rent percent, 2019 mean per CBSA',
    #                 highlight=True).add_to(map1)
    
    # # add hover data
    # style_function = lambda x: {'fillColor': '#ffffff', 
    #                         'color':'#000000', 
    #                         'fillOpacity': 0.1, 
    #                         'weight': 0.1}
    # highlight_function = lambda x: {'fillColor': '#000000', 
    #                                 'color':'#000000', 
    #                                 'fillOpacity': 0.50, 
    #                                 'weight': 0.1}
    # pop_data = folium.features.GeoJson(
    #     agg_CBSA_mapdf,
    #     style_function=style_function, 
    #     control=False,
    #     highlight_function=highlight_function, 
    #     tooltip=folium.features.GeoJsonTooltip(
    #         fields=['rent_pct','pop_2019_est'],
    #         aliases=['mean rent percent of house prices: ','2019 estimated population: '],
    #         style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") 
    #     )
    # )
    # map1.add_child(pop_data)
    # map1.keep_in_front(pop_data)
    # folium.LayerControl().add_to(map1)
    #return map1._repr_html_()
    #map1.save('templates/map.html')
    return render_template('../templates/index.html')

if __name__ == '__main__':
    # testing
    #app.run(debug=True)
    # production:
    app.run(port=33507)