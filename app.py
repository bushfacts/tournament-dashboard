import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
#save in browser somewhere the event chosen and use that to rotate datasets

unitStats = json.loads(open("data/unitStats.json").read())
unitIDs = [[unit,unitStats[unit]['name']] for unit in unitStats]
unitIDs.sort(key=lambda x:x[1]) #alphabetical sort
factionStats = json.loads(open("data/factionStats.json").read())
factionColorsHex = {'rebel': '#A91515', 'imperial': '#6B6B6B',
                    'republic': 'C49D36', 'separatist': '101A48'}

app = dash.Dash(__name__)
server = app.server

#build out any static graphs up here and then drop them into app.layout below
labels = [faction['name'] for faction in factionStats]
values = [faction['count'] for faction in factionStats]
factionFig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'textinfo': 'value',
            'marker': {'colors':[factionColorsHex[label] for label in labels]}}]}

app.layout = html.Div([
                dcc.Tabs(id='navigation', value='summary', children=[
                    dcc.Tab(label='Summary', value='summary', children=[
                        dcc.Graph(figure=factionFig)
                    ]),
                    dcc.Tab(label='Factions', value='faction', children=[
                        html.H2('faction tab')
                    ]),
                    dcc.Tab(label='Units', value='units', children=[
                        dcc.Dropdown(id='unit-selection',
                            options=[{'label':unit[1],'value':int(unit[0])} for unit in unitIDs],
                            value=int(unitIDs[0][0])),
                        html.Div(id='graph')
                    ]),
                    dcc.Tab(label='Meta Lists',children=[
                        html.H2('meta lists tab')
                    ])
                ]),
                html.Img(src=app.get_asset_url('BushFacts white.png'), width="303px", height="75px")
            ])

@app.callback(
    Output('graph', 'children'),
    [Input('unit-selection', 'value')])
def update_figure(select):
    traces = []
    unitID = str(select)
    unitName = unitStats[unitID]['name']
    unitCount = int(unitStats[unitID]['count'])
    unitRank =  unitStats[unitID]['rank']
    for type in unitStats[unitID]['upgrades']:
        data = [{'name':upgrade, 'count':int(unitStats[unitID]['upgrades'][type][upgrade])} for upgrade in unitStats[unitID]['upgrades'][type]]
        data.sort(reverse=True, key=lambda x:x['count'])
        labels = [upgrade['name'] for upgrade in data]
        values = [upgrade['count'] for upgrade in data]
        traces.append({
            'x':labels,
            'y':values,
            'type':'bar',
            'name':type.title()
        })
    return html.Div(dcc.Graph(id='test',
        figure={
            'data': traces,
            'layout': {
                'yaxis': {'range': [0,unitCount]},
                'transition': {'duration': 500},
                'title': unitName + "<br>" + str(unitCount) + " in attendance"
            }
        }
    ))


if __name__ == '__main__':
    app.run_server(debug=True)
