import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import plotly-express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
df = px.data.tips()
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

infla = pandas.read_csv(r"inflation.csv")
unemp = pandas.read_csv(r"unemployment.csv")
gdp = pandas.read_csv(r"gdp.csv")
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='GDP Trends', children=[
            html.P("Year:"),
                dcc.Graph(id="pie-chart"),
                dcc.Slider(
                    id='year',
                    min=0,
                    max=7,
                    marks={i: gdp['Year'].tolist()[i] for i in range(7)},
                    value=3,
                ),
        ]),
        dcc.Tab(label='Unemployment Rates', children=[
            dcc.Graph(
                figure=dict(
                    data=[
                        dict(
                            x= unemp['year'].tolist(),
                            y= unemp['Japan'].tolist(),
                            name='Japan',
                            marker=dict(
                                color='rgb(88, 204, 237)'
                            )
                        ),
                        dict(
                            x= unemp['year'].tolist(),
                            y= unemp['usa'].tolist(),
                            name='USA',
                            marker=dict(
                                color='rgb(18, 97, 160)'
                            )
                        ),
                        dict(
                            x= unemp['year'].tolist(),
                            y= unemp['India'].tolist(),
                            name='India',
                            marker=dict(
                                color='rgb(7, 47, 95)'
                            )
                        ),
                        dict(
                            x= unemp['year'].tolist(),
                            y= unemp['germany'].tolist(),
                            name='Germany',
                            marker=dict(
                                color='rgb(56, 149, 211)'
                            )
                        ),

                    ],
                    layout=dict(
                        title='Unemployment Rate',
                        showlegend=True,
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=50, b=30)
                    )
                ),
                style={'height': 400},
                id='my-graph-1'
            )
        ]),
        dcc.Tab(label='Inflation Rates', children=[
            dcc.Graph(
                figure=dict(
                    data=[
                        dict(
                            x= infla['year'].tolist(),
                            y= infla['Japan'].tolist(),
                            name='Japan',
                            marker=dict(
                                color='rgb(88, 204, 237)'
                            )
                        ),
                        dict(
                            x= infla['year'].tolist(),
                            y= infla['USA'].tolist(),
                            name='USA',
                            marker=dict(
                                color='rgb(18, 97, 160)'
                            )
                        ),
                        dict(
                            x= infla['year'].tolist(),
                            y= infla['India'].tolist(),
                            name='India',
                            marker=dict(
                                color='rgb(7, 47, 95)'
                            )
                        ),
                        dict(
                            x= infla['year'].tolist(),
                            y= infla['germany'].tolist(),
                            name='Germany',
                            marker=dict(
                                color='rgb(56, 149, 211)'
                            )
                        ),

                    ],
                    layout=dict(
                        title='Inflation Rate',
                        showlegend=True,
                        legend=dict(
                            x=0,
                            y=1.0
                        ),
                        margin=dict(l=40, r=0, t=50, b=30)
                    )
                ),
                style={'height': 400},
                id='my-graph'
            )
        ]),
    ])
])


@app.callback(
    Output("pie-chart", "figure"),
    [Input("year", "value")])
def generate_chart(year):
    labels = ['Primary/Agriculture', 'Secondary/Industrial', 'Tertiary/Services']
    # Define color sets of paintings
    night_colors = ['rgb(105, 190, 40)', 'rgb(255, 136, 73)', 'rgb(61, 183, 228)']

    # Create subplots, using 'domain' type for pie charts
    specs = [[{'type': 'domain'}, {'type': 'domain'}], [{'type': 'domain'}, {'type': 'domain'}]]
    fig = make_subplots(rows=2, cols=2, specs=specs, subplot_titles=['India', 'Bangladesh','China','Japan'])

    # Define pie charts
    fig.add_trace(go.Pie(labels=labels, values=gdp.iloc[year][1:4], name='India',
                         marker_colors=night_colors), 1, 1)
    fig.add_trace(go.Pie(labels=labels, values=gdp.iloc[year].tolist()[4:7], name='Bangladesh',
                         marker_colors=night_colors), 1, 2)
    fig.add_trace(go.Pie(labels=labels, values=gdp.iloc[year].tolist()[7:10], name='China',
                         marker_colors=night_colors), 2, 1)
    fig.add_trace(go.Pie(labels=labels, values=gdp.iloc[year].tolist()[10:13], name='Japan',
                         marker_colors=night_colors), 2, 2)

    # Tune layout and hover info
    fig.update_traces( hoverinfo='label+percent+name', textinfo='percent')
    fig.update(layout_title_text='Sector-wise GDP distribution',
               layout_showlegend=True)
    return fig


if __name__ == '__main__':
    app.run_server()
