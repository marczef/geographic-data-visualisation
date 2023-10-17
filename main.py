from dash import Dash, html, dcc, callback, Output, Input, no_update

from utils import *

app = Dash(__name__)

app.layout = html.Div(
    [
        html.Div("title template", id="title", className="title"),
        html.P("Wybierz zanieczyszczenie:", className="text"),
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
                   value=2020,
                   className="slider"
                   ),
        html.Div(
            [
                dcc.Dropdown(
                    id="pollution",
                    options=load_pollution_names(),
                    placeholder="Select a pollution",
                    className="dropdown"
                ),
                dcc.RadioItems(
                    id="type_of_plotting",
                    options=["per km square", "overall"],
                    inline=True,
                    value="per km square",
                    className="radio"
                ),
            ],
            className="row",
        ),
        dcc.Graph(id="graph", className="graph", figure=blank_fig()),
    ]
)

@app.callback(
    Output("graph", "figure"),
    Input("pollution", "value"),
    Input("slider_year", "value"),
    Input("type_of_plotting", "value")
)
def map_plot(pollution, slider_year, type_of_plotting):
    try:
        url = "data/pollution_coordinates.geojson"
        districts = gpd.read_file(url)

        if type_of_plotting == "overall":
            data_name = (pollution + "_" + str(slider_year))
        elif type_of_plotting == "per km square":
            data_name = (pollution + "_" + str(slider_year) + "_per_km_sq")
        else:
            return no_update

        fig = px.choropleth(
            districts,
            geojson=districts.geometry,
            locations="id",
            color=data_name,
            projection="mercator",
            color_continuous_scale='RdYlGn_r',
            hover_name="nazwa",
            hover_data={data_name: True, "id": False},
            labels={data_name: ""},
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
        )

        return fig

    except:
        return no_update


if __name__ == '__main__':
    # init_data()
    app.run(debug=True)
