from flask import Flask, render_template
import folium
import pandas as pd
import geopandas as gpd
import boto3
import s3fs

app = Flask(__name__, root_path='../app_engine') # template_folder='../app_engine/templates'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cover')
def cover():
    return render_template('cover.html')

if __name__ == '__main__':
    # testing
    app.run(host='0.0.0.0', port=33507, threaded=True, debug=True)
    # production:
    #app.run(host='0.0.0.0', port=33507, threaded=True)