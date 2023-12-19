from dash import Dash, html, dcc, callback, Output, Input, State, no_update, ctx
import geopandas as gpd

from utils import  *

clicked_locations = []
actual_gas = ""

app = Dash(__name__)
server = app.server

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Div(className="cloud"),
                    ],
                    className="x1",
                ),
                html.Div(
                    [
                        html.Div(className="cloud"),
                    ],
                    className="x2",
                ),
                html.Div(
                    [
                        html.Div(className="cloud"),
                    ],
                    className="x3",
                ),
                html.Div(
                    [
                        html.Div(className="cloud"),
                    ],
                    className="x4",
                ),
                html.H1("Całkowita emisja wybranych gazów cieplarnianych", id="title", className="title"),
                dcc.Slider(min=2016, max=2021,
                           step=None,
                           marks={
                               2016: '2016',
                               2017: '2017',
                               2018: '2018',
                               2019: '2019',
                               2020: '2020',
                               2021: '2021',
                           },
                           id='slider_year',
                           value=2021,
                           className="slider",
                           ),
                html.Div(
                    [
                        dcc.Dropdown(
                            id="pollution",
                            options=[
                                {'label': 'dwutlenek węgla', 'value': 'co2'},
                                {'label': 'metan', 'value': 'metan'},
                                {'label': 'podtlenek azotu', 'value': 'n2o'},
                                {'label': 'dwutlenek siarki', 'value': 'so2'},
                                {'label': 'tlenek azotu', 'value': 'no'},
                                {'label': 'tlenek węgla', 'value': 'co'},
                            ],
                            placeholder="Wybierz rodzaj gazu",
                            className="dropdown"
                        ),
                        dcc.RadioItems(
                            id="type_of_plotting",
                            options=[
                                {'label': "tyś. ton na km\u00b2", 'value': "square"},
                                {'label': "tyś. ton na woj.", 'value': "overall"}
                            ],
                            inline=True,
                            value="square",
                            className="radio"
                        ),
                    ],
                    className="row",
                ),
                dcc.Graph(id="graph", className="graph", figure=blank_fig()),
                html.Div([
                    html.Div("Zaznacz województwa, z których chcesz wyliczyć średnią", id="text_1", className="text_1"),
                    html.Div(
                        id='av_woj',
                        className='av_woj'
                    ),
                    html.Button("Wylicz", id='submit_val', className='submit_val'),
                    html.Div(
                        id="pom_div_avg"
                    )
                ],
                    className="av_woje"),
                html.Div([
                    html.Div("Zaznacz lata (i województwa, z których chcesz wyliczyć średnią.", className="text_2"),
                    dcc.Checklist(
                       options=[
                           {'label': '2016', 'value': '2016'},
                           {'label': '2017', 'value': '2017'},
                           {'label': '2018', 'value': '2018'},
                           {'label': '2019', 'value': '2019'},
                           {'label': '2020', 'value': '2020'},
                           {'label': '2021', 'value': '2021'},
                       ],
                       value=['2021'],
                       id='checklist_years',
                       inline=True,
                       className='checklist_years'
                    ),
                    html.Button("Dla całego kraju", id='submit_val_year1', className="submit_val_year1"),
                    html.Button("Dla określonych woj", id='submit_val_year2', className="submit_val_year2"),
                    html.Div(
                        id="pom_div_avg_year",
                        className="pom_div_avg_year"
                    )
                ],
                    className="av_year"),
            ],
            className="background-wrap",
        ),
    ],
)

@callback(
    Output('pom_div_avg', 'children'),
    Input('submit_val', 'n_clicks'),
    prevent_initial_call=True
)
def update_avg_voi(n_clicks):
    return count_avg_by_voivodeship(clicked_locations, actual_gas)

@callback(
    Output('pom_div_avg_year', 'children'),
    State("pollution", "value"),
    State("type_of_plotting", "value"),
    State("checklist_years", "value"),
    Input("submit_val_year1", "n_clicks"),
    Input("submit_val_year2", "n_clicks"),
    prevent_initial_call=True
)
def update_avg_year(pollution, type_of_plotting, years, n_clicks1, n_clicks2):
    button_clicked = ctx.triggered_id

    if button_clicked == "submit_val_year1":
        return count_avg_by_year(years, pollution, type_of_plotting, [])
    elif button_clicked == "submit_val_year2":
        if not clicked_locations:
            return
        else:
            return count_avg_by_year(years, pollution, type_of_plotting, clicked_locations)

@app.callback(
    Output('av_woj', 'children'),
    [Input('graph', 'clickData')])
def return_avr_voi(click_data):
    if click_data is not None:
        location = click_data['points'][0]['location']

        if location not in clicked_locations:
            clicked_locations.append(location)
        else:
            clicked_locations.remove(location)
        return
    else:
        clicked_locations.clear()


@app.callback(
    Output("graph", "figure"),
    Input("pollution", "value"),
    Input("slider_year", "value"),
    Input("type_of_plotting", "value"),
    Input('graph', 'clickData')
)
def map_plot(pollution, slider_year, type_of_plotting, click_data):
    try:
        districts = gpd.read_file(absolute_path)

        global actual_gas

        if type_of_plotting == "overall":
            actual_gas = (pollution + "_" + str(slider_year))
        elif type_of_plotting == "square":
            actual_gas = (pollution + "_" + str(slider_year) + "_per_km_sq")
        else:
            return no_update

        fig = px.choropleth(
            districts,
            geojson=districts.geometry,
            locations="id",
            color=actual_gas,
            projection="conic conformal",
            color_continuous_scale='RdYlGn_r',
            hover_name="nazwa",
            hover_data={actual_gas: True, "id": False},
            labels={actual_gas: ""},
        )
        fig.update_geos(fitbounds="locations", visible=False)
        fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0},
                          coloraxis_colorbar_x=0.75,
                          geo=dict(bgcolor='rgba(0,0,0,0)'),
                          paper_bgcolor='rgba(0,0,0,0)',
                          )
        fig.update_traces(marker_line_width=0)

        if ctx.triggered[0]['prop_id'] == 'graph.clickData':
            width = [2 if i in clicked_locations else 0 for i in range(len(fig.data[0]["locations"]))]
            fig.update_traces(
                marker=dict(line=dict(width=width)),
                selector=dict(type='choropleth'))

        return fig

    except:
        return no_update


if __name__ == '__main__':
    # init_data(absolute_path_init, absolute_path, absolute_path_excel)
    app.run_server(debug=True)
