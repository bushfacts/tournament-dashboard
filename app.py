import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
unitStats = json.loads(open("data/unitStats.json").read())
unitIDs = [[unit,unitStats[unit]['name']] for unit in unitStats]
unitIDs.sort(key=lambda x:x[1]) #alphabetical sort

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dcc.Graph(id='main-graph'),
    dcc.Dropdown(
                id='unit-name',
                options=[{'label': unit[1], 'value': unit[0]} for unit in unitIDs],
                value=unitIDs[0][0]
            )
])

@app.callback(
    Output('main-graph', 'figure'),
    [Input('unit-name', 'value')])
def update_figure(unitID):
    fig = go.Figure()
    traces = []
    unitName = unitStats[unitID]['name']
    unitCount = int(unitStats[unitID]['count'])
    unitRank =  unitStats[unitID]['rank']
    # data = [{'name':unitStats[unitID]['upgrades']['name'], 'count':unitStats[unitID]['upgrades']['count']} for upgrade in unitStats[unitID]['upgrades']]
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

    # df = pd.read_csv('data/units/upgrades/' + str(selected_unitID) + ".csv")
    # data = [{'values': [i for i in df['count']], 'labels': [i for i in df['upgrades']], 'type': 'pie', 'title': unitName + ": " + str(unitCount) + "\n", 'textinfo': ('label+value')}]

    return {
        'data': traces,
        'layout': {
            'yaxis': {'range': [0,unitCount]},
            'transition': {'duration': 500},
            'title': unitName
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)
