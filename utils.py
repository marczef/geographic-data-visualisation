import geopandas as gpd
import numpy as np
import plotly.express as px
import pandas as pd
from numpyencoder import NumpyEncoder
import json
import plotly.graph_objects as go
from plotly.graph_objs import *

absolute_path = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\data\pollution_coordinates.geojson'
absolute_path_init = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\data\wojewodztwa-min.geojson'
absolute_path_excel = r'C:\Users\User\OneDrive\Pulpit\Marcysia\github\visualisation_geographic_data\data\pollution_data.xlsx'


def init_data(init_geojson_path, path_geojson, excel_path):
    try:
        with open(init_geojson_path, 'r') as f:
            data_geojson = json.load(f)
        data = pd.ExcelFile(excel_path)

    except json.JSONDecodeError as e:
        raise json.JSONDecodeError("Invalid JSON syntax", e.doc, e.pos)

    except:
        raise TypeError("Invalid path")

    add_area(data_geojson, data)
    add_data_absolute(data_geojson, data)
    add_data_per_km2(data_geojson, data)

    save_data(path_geojson, data_geojson)


def save_data(path, data_geojson):
    try:
        with open(path, 'w') as f:
            json.dump(data_geojson, f, cls=NumpyEncoder)
    except:
        raise TypeError("Unable to serialize the object")


def add_area(data_geojson, data): #adding area of voivodeship from excel to geojson
    try:
        df1 = pd.read_excel(data, 'data2020')
        df = pd.DataFrame(df1)
    except:
        raise TypeError("Invalid path")

    try:
        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    feat['properties']['area'] = df['area'][woj]
    except:
        raise ValueError("Invalid field")


def add_data_per_km2(data_geojson, data): #adding a field in geojson with relative value
    for year in ['2020', '2019', '2018', '2017', '2016']:
        try:
            df1 = pd.read_excel(data, 'data' + year)
            df = pd.DataFrame(df1)
        except:
            raise TypeError("Didn't find file or sheet")

        try:
            for feat in data_geojson['features']:
                for woj in range(len(df["woj."])):
                    if feat["properties"]["nazwa"] == df["woj."][woj]:
                        for pol in list(df.columns)[2:]:
                            feat['properties'][str(pol) + "_" + year + "_per_km_sq"] = df[pol][woj].item() / df['area'][woj].item()
        except ZeroDivisionError:
            raise ZeroDivisionError("Cannot divide by zero")
        except:
            raise ValueError("Invalid field")


def add_data_absolute(data_geojson, data):
    for year in ['2020', '2019', '2018', '2017', '2016']:
        try:
            df1 = pd.read_excel(data, 'data' + year)
            df = pd.DataFrame(df1)
        except:
            raise TypeError("Didn't find file or sheet")

        try:
            for feat in data_geojson['features']:
                for woj in range(len(df["woj."])):
                    if feat["properties"]["nazwa"] == df["woj."][woj]:
                        for pol in list(df.columns)[2:]:
                            feat['properties'][str(pol) + "_" + year] = df[pol][woj]
        except:
            raise ValueError("Invalid field")

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


def count_avg_by_voivodeship(ids, gas): #counting average data of some voivodeships
    if not ids or not gas or not all(isinstance(i, int) for i in ids):
        return
    if not all(0 <= i <= 15 for i in ids):
        return
    with open(absolute_path, 'r') as f:
        data_geojson = json.load(f)
    try:
        avg = 0
        for feat in data_geojson['features']:
            if feat["id"] in ids:
                avg += feat["properties"][gas]

        return round(avg / len(ids), 5)

    except:
        return None


def count_avg_by_year(years, gas, type_of_ploting, ids): #counting average data of some years
    if not years or not gas or not type_of_ploting or not all(isinstance(i, int) for i in ids):
        return
    if not all(0 <= i <= 15 for i in ids):
        return
    if len(ids) == 0:
        ids = [i for i in range(0, 16)]
    with open(absolute_path, 'r') as f:
        data_geojson = json.load(f)

    try:
        avg = 0
        for year in years:
            if type_of_ploting == "overall":
                gas_now = (gas + "_" + year)
            elif type_of_ploting == "square":
                gas_now = (gas + "_" + year + "_per_km_sq")

            for feat in data_geojson['features']:
                if feat["id"] in ids:
                    avg += feat["properties"][gas_now]
        return round(avg / (len(ids) * len(years)), 5)

    except:
        return None
