import geopandas as gpd
import numpy as np
import plotly.express as px
import pandas as pd
from numpyencoder import NumpyEncoder
import json
import plotly.graph_objects as go
from plotly.graph_objs import *


def init_data():
    with open('data/wojewodztwa-min.geojson', 'r') as f:
        data_geojson = json.load(f)
    data = pd.ExcelFile(r"data/pollution_data.xlsx")

    add_area(data_geojson, data)

    for year in ['2020', '2019', '2018', '2017', '2016']:
        df1 = pd.read_excel(data, 'data' + year)
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
        df1 = pd.read_excel(data, 'data' + year)
        df = pd.DataFrame(df1)

        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    for pol in list(df.columns)[2:]:
                        feat['properties'][str(pol) + "_" + year + "_per_km_sq"] = df[pol][woj] / df['area'][woj]


def load_pollution_names():
    data = pd.read_excel(r"data\pollution_data.xlsx")
    df = pd.DataFrame(data)

    return [pol for pol in list(df.columns)[2:]]


def blank_fig():
    layout = Layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig = go.Figure(go.Scatter(x=[], y=[]), layout=layout)
    fig.update_layout(template=None)
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
    fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
    return fig


def count_avg_by_voivodeship(ids, gas):
    if not ids:
        return "Nie podano danych"
    with open('data/pollution_coordinates.geojson', 'r') as f:
        data_geojson = json.load(f)

    avg = 0
    for feat in data_geojson['features']:
        if feat["id"] in ids:
            avg += feat["properties"][gas]

    return avg / len(ids)


def count_avg_by_year(years, gas, type_of_ploting, ids):
    if not years:
        return "Nie podano danych"
    if len(ids) == 0:
        ids = [i for i in range(0, 16)]
    with open('data/pollution_coordinates.geojson', 'r') as f:
        data_geojson = json.load(f)

    avg = 0

    for year in years:
        if type_of_ploting == "overall":
            gas_now = (gas + "_" + year)
        elif type_of_ploting == "square":
            gas_now = (gas + "_" + year + "_per_km_sq")

        for feat in data_geojson['features']:
            if feat["id"] in ids:
                avg += feat["properties"][gas_now]

    return avg / (len(ids) * len(years))
