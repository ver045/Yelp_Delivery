from flask import Flask, render_template,request
import plotly
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json

app = Flask(__name__)

@app.route('/')
def index():
    feature = 'Daly City'
    bar = create_plot(feature)
    return render_template('index.html', plot = bar)

def create_plot(feature):
    dc_takeout_df = pd.read_csv("dc_takeout.csv")
    sb_takeout_df = pd.read_csv("sb_takeout.csv")
    mlbr_takeout_df = pd.read_csv("mlbr_takeout.csv")
    sf_takeout_df = pd.read_csv("sf_takeout.csv")
    ssf_takeout_df = pd.read_csv("ssf_takeout.csv")
    dc_takeout_df['city'] = "Daly City"
    sb_takeout_df['city'] = "San Bruno"
    mlbr_takeout_df['city'] = "Milbrae"
    sf_takeout_df['city'] = "San Francisco"
    ssf_takeout_df['city'] = "South San Francisco"

    dfs = [dc_takeout_df, sb_takeout_df, mlbr_takeout_df, sf_takeout_df, ssf_takeout_df]

    all_cities = pd.concat(dfs, ignore_index=True, sort=True)

    all_city_price_counts = all_cities.groupby(['city', 'price'])['id'].count().to_frame().reset_index().rename({'id' : 'count'}, axis = 1)

    if feature == 'Daly City':
        data = [go.Bar(x=list(all_city_price_counts.price.unique()), y=all_city_price_counts['count'][0:2])]
    elif feature == 'Milbrae':
        data = [go.Bar(x=list(all_city_price_counts.price.unique()), y=all_city_price_counts['count'][2:4])]
    elif feature == 'San Bruno':
        data = [go.Bar(x=list(all_city_price_counts.price.unique()), y=all_city_price_counts['count'][4:7])]
    elif feature == 'San Francisco':
        data = [go.Bar(x=list(all_city_price_counts.price.unique()), y=all_city_price_counts['count'][7:9])]
    else:
        data = [go.Bar(x=list(all_city_price_counts.price.unique()), y=all_city_price_counts['count'][9:-1])]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    
    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():
    feature = request.args['selected']
    graphJSON= create_plot(feature)
    return graphJSON


@app.route("/dalycity")
def dalycitymap():
    return render_template("daly_city.html")

@app.route("/millbrae")
def millbraemap():
    return render_template("millbrae.html")


@app.route("/sanbruno")
def sanbrunomap():
    return render_template("san_bruno.html")


@app.route("/sf")
def sfmap():
    return render_template("sf.html")


@app.route("/southsf")
def southsfmap():
    return render_template("south_sf.html")


if __name__ == '__main__':
    app.run(debug=True)