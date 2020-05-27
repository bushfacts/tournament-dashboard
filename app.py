import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json
#save in browser somewhere the event chosen and use that to rotate datasets

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
unitStats = json.loads(open("data/unitStats.json").read())
unitIDs = [[unit,unitStats[unit]['name']] for unit in unitStats]
unitIDs.sort(key=lambda x:x[1]) #alphabetical sort

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
# app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
                html.Div([
                    dcc.Dropdown(
                        id='first-selection',
                        options=[{'label':'Summary','value':1},{'label':'Factions','value':2},{'label':'Units','value':3}],
                        value=3
                    ),
                    dcc.Dropdown(
                        id='second-selection',
                    )],
                    style={'width':'350px', 'display':'inline-block'}
                    ),
                html.Div(
                    dcc.Graph(id='main-graph'), style={'width':'80%','display':'inline-block'})
])

@app.callback(
    [Output('second-selection', 'options'),
    Output('second-selection','value')],
    [Input('first-selection', 'value')])
def updateSecondMenu(selection):
    if selection == 3: #unit drop down options
        options = [{'label': unit[1], 'value': int(unit[0])} for unit in unitIDs]
        value = unitIDs[0][0]
    else:
        options = [{'label': 'you', 'value': 1}, {'label': 'suck', 'value': 2}]
        value = 1
    return options, value

#take two inputs. one from each dropdown to figure out what graph to present
@app.callback(
    Output('main-graph', 'figure'),
    [Input('first-selection', 'value'),
    Input('second-selection', 'value')])
def update_figure(select1, select2):
    if select1 == 3:
        # fig = go.Figure()
        traces = []
        unitID = str(select2)
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
        return {
            'data': traces,
            'layout': {
                'yaxis': {'range': [0,unitCount]},
                'transition': {'duration': 500},
                'title': unitName + "<br>" + str(unitCount) + " in attendance"
            }
        }
    else:
        return {'data':[1,2,3]}

if __name__ == '__main__':
    app.run_server(debug=True)
