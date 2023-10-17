import geopandas as gpd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
from numpyencoder import NumpyEncoder
import json
import plotly.graph_objects as go

def init_data():
    with open('data/wojewodztwa-min.geojson', 'r') as f:
        data_geojson = json.load(f)
    data = pd.ExcelFile(r"data/pollution_data.xlsx")

    add_area(data_geojson, data)

    for year in ['2020', '2019', '2018', '2017', '2016']:
        df1 = pd.read_excel(data, 'data'+year)
        df = pd.DataFrame(df1)

        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    for pol in list(df.columns)[2:]:
                        feat['properties'][str(pol) + "_" + year] = df[pol][woj]

    add_data_per_km2(data_geojson, data)

    with open('data/pollution_coordinates.geojson', 'w') as f:
        json.dump(data_geojson, f, cls=NumpyEncoder)


def add_area(data_geojson, data):
    df1 = pd.read_excel(data, 'data2020')
    df = pd.DataFrame(df1)

    for feat in data_geojson['features']:
        for woj in range(len(df["woj."])):
            if feat["properties"]["nazwa"] == df["woj."][woj]:
                feat['properties']['area'] = df['area'][woj]


def add_data_per_km2(data_geojson, data):
    for year in ['2020', '2019', '2018', '2017', '2016']:
        df1 = pd.read_excel(data, 'data'+year)
        df = pd.DataFrame(df1)

        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    for pol in list(df.columns)[2:]:
                        feat['properties'][str(pol) + "_" + year + "_per_km_sq"] = df[pol][woj]/df['area'][woj]


def load_pollution_names():
    data = pd.read_excel(r"data\pollution_data.xlsx")
    df = pd.DataFrame(data)

    return [pol for pol in list(df.columns)[2:]]


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y=[]))
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)

    return fig