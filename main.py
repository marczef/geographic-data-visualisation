from dash import Dash, html, dcc, callback, Output, Input

from utils import *

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H1("title template"),
        html.P("Wybierz zanieczyszczenie:"),
        dcc.Slider(min=2016, max=2020,
                   step=None,
                   marks={
                       2016: '2016',
                       2017: '2017',
                       2018: '2018',
                       2019: '2019',
                       2020: '2020',
                   },
                   id='slider_year',
                   value=2020
                   ),
        dcc.RadioItems(
            id="pollution",
            options=load_pollution_names(),
            value="co2",
            inline=True,
        ),
        dcc.Graph(id="graph"),
    ]
)
@app.callback(
    Output("graph", "figure"),
    Input("pollution", "value"),
    Input("slider_year", "value"),
)
def map_plot(pollution, slider_year):
    url = "data/pollution_coordinates.geojson"

    districts = gpd.read_file(url)

    data_name = (pollution+"_"+str(slider_year))

    fig = px.choropleth(
        districts,
        geojson=districts.geometry,
        locations="id",
        color=data_name,
        projection="mercator",
        color_continuous_scale = 'RdYlGn_r',
        hover_name="nazwa",
        hover_data={data_name: True, "id": False},
    )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

    return fig


if __name__ == '__main__':
    app.run(debug=True)
    # init_data()