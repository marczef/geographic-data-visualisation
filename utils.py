import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
import pandas as pd
import json

def init_data():
    with open('data/wojewodztwa-min.geojson', 'r') as f:
        data_geojson = json.load(f)

    for year in ['2020', '2019', '2018', '2017', '2016']:

        data = pd.ExcelFile(r"data/pollution_data.xlsx")

        df1 = pd.read_excel(data, 'data'+year)
        df = pd.DataFrame(df1)

        for feat in data_geojson['features']:
            for woj in range(len(df["woj."])):
                if feat["properties"]["nazwa"] == df["woj."][woj]:
                    for pol in list(df.columns)[1:]:
                        feat['properties'][str(pol)+"_"+year] = df[pol][woj]

    with open('data/pollution_coordinates.geojson', 'w') as f:
        json.dump(data_geojson, f)

def load_pollution_names():
    data = pd.read_excel(r"data\pollution_data.xlsx")
    df = pd.DataFrame(data)

    return [pol for pol in list(df.columns)[1:]]