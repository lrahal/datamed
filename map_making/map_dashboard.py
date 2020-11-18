import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import plotly.express as px
from dash.dependencies import Input, Output

from map_making.get_maps_data import get_final_dataframe, get_single_site_api

external_scripts = [
    {
        'src': 'https://code.jquery.com/jquery-3.5.1.slim.min.js',
        'integrity': '',
        'crossorigin': 'anonymous'
    },
    {
        'src': 'https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js',
        'integrity': '',
        'crossorigin': 'anonymous'
    }
]

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'type': 'text/css',
        'integrity': '',
        'crossorigin': 'anonymous'
    }
]


app = dash.Dash(__name__, external_scripts=external_scripts, external_stylesheets=external_stylesheets)
app.title = 'Cartographie des sites de fabrication de médicaments'

df, df_countries = get_final_dataframe()
df_countries['text'] = df_countries['country'] + ': ' + df_countries['substance_active'].astype(str)

single_site_api_list = get_single_site_api(df)

fig_world_map = px.scatter_geo(df_countries,
                               # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                               lon='longitude',
                               lat='latitude',
                               # style
                               color='country',
                               size='substance_active',
                               # choose the map chart's projection
                               projection='natural earth',
                               # columns which is in bold in the pop-up
                               hover_name='text',
                               # format of the pop-up not to display these columns' data
                               hover_data={
                                   'country': False, 'longitude': False, 'latitude': False, 'substance_active': False
                               }
                               )
fig_world_map.update_geos(fitbounds='locations', showcountries=True)
fig_world_map.update_layout(clickmode='event+select')

# fig_world_map = go.Figure(data=go.Scattergeo(
#     lon=df_countries['longitude'],
#     lat=df_countries['latitude'],
#     text=df_countries['text'],
#     mode='markers',
#     marker_color=df_countries['substance_active'],
# ))
#
# fig_world_map.update_layout(
#         title='Most trafficked US airports<br>(Hover for airport names)',
#         geo_scope='world',
#     )

columns = ['denomination_specialite', 'cis', 'substance_active', 'country']

app.layout = html.Div(className='container-fluid', children=[
    html.Div([
        html.H1('DASH - ANSM DATA APP')]),
    dcc.Tabs([
        dcc.Tab(label='Overview', children=[
            html.Div([
                html.H2('Cartographie des sites de fabrication de substances actives', style={'margin-top': 30})]),
            html.P('Sélectionnez un pays pour afficher les différentes substances actives qui y sont fabriquées'),
            dcc.Graph(id='world-graph', figure=fig_world_map),
            dash_table.DataTable(
                columns=[{'name': col, 'id': col} for col in columns],
                data=[],
                id='click-data',
                page_size=10,
                style_table={'height': '300px', 'overflowY': 'auto'},
                style_as_list_view=True,
                style_cell={'padding': '5px', 'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                })
        ]),

        dcc.Tab(label='Détection des API à risque', children=[
            html.Div([
                html.H2('Substances actives fabriquées dans un unique site')],
                style={'textAlign': 'left', 'padding-bottom': '30', 'margin-top': 30}),
            html.P("Liste des substances actives fabriquées dans un seul site (pas d'alternative)"),
            dash_table.DataTable(
                    columns=[{'name': col, 'id': col} for col in ['substance_active', 'formatted_address', 'country']],
                    data=single_site_api_list,
                    filter_action='native',
                    sort_action='native',
                    page_size=15,
                    style_table={'height': '400px', 'overflowY': 'auto'},
                    style_as_list_view=True,
                    style_cell={'padding': '5px', 'textAlign': 'left'},
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    }),
            html.Div([html.H2('Sites de fabrication par substance active', style={'margin-top': 60})],
                     style={'textAlign': 'left', 'padding-bottom': '30'}),
            html.P('Sélectionnez une substance active pour voir dans quels sites elle est fabriquée'),
            dcc.Dropdown(
                id='api-dropdown',
                options=[{'label': api, 'value': api} for api in sorted(df.substance_active.unique())],
                value='abacavir'
            ),
            dcc.Graph(id='api-graph')
        ])
    ])
])


@app.callback(Output('click-data', 'data'), Input('world-graph', 'clickData'))
def update_table(clickData):
    if not clickData:
        return []
    country_name = clickData['points'][0]['customdata'][0]
    print(country_name)
    return df[df.country == country_name].sort_values(by=['substance_active']).to_dict('records')


@app.callback(Output('api-graph', 'figure'), [Input('api-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    # set up the chart from the df dataframe
    fig = px.scatter_geo(df[df.substance_active == selected_dropdown_value],
                         # longitude is taken from the df['longitude'] columns and latitude from df['latitude']
                         lon='longitude',
                         lat='latitude',
                         # style
                         color='country',
                         # choose the map chart's projection
                         projection='natural earth',
                         # columns which is in bold in the pop-up
                         hover_name='cis',
                         # format of the pop-up not to display these columns' data
                         hover_data={'cis': False, 'longitude': False, 'latitude': False}
                         )
    fig.update_traces(marker=dict(size=10))
    fig.update_geos(fitbounds='locations', showcountries=True)
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
