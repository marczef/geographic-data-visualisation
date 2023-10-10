from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

from map_visualisation import *

df = px.data.election()

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Przykładowy tytuł strony"),
        html.P("Wybierz zanieczyszczenie:"),
        dcc.RadioItems(
            id="pollution",
            options=["carbon_dioxide", "carbon_dioxide_tons_by_sq_km"],
            value="carbon_dioxide",
            inline=True,
        ),
        dcc.Graph(id="graph"),
    ]
)
@app.callback(
    Output("graph", "figure"),
    Input("pollution", "value"),
)
def map_plot(pollution):
    url = "data/wojewodztwa-min.geojson"

    districts = gpd.read_file(url)
    # districts = districts.to_crs("WGS84")

    fig = px.choropleth(
        districts,
        geojson=districts.geometry,
        locations = "id",
        color=pollution,
        projection="mercator",
        color_continuous_scale = 'RdYlGn_r',
        hover_name="nazwa",
        hover_data={pollution: True, "id": False},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':

    app.run(debug=True)