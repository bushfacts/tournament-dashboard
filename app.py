#need bar widths to be relative to the screen, not number of categories...

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import json

########################################################################
############################ STATIC OBJECTS ############################
########################################################################

#save in browser somewhere the event chosen and use that to rotate datasets

unitStats = json.loads(open("data/unitStats.json").read())
unitIDs = [[unit,unitStats[unit]['name']] for unit in unitStats]
unitIDs.sort(key=lambda x:x[1]) #alphabetical sort
summaryStats = json.loads(open("data/summaryStats.json").read())
colors = {'rebel': '#A91515', 'imperial': '#6B6B6B',
                    'republic': 'C49D36', 'separatist': '101A48'}
#choose a color for each gear

app = dash.Dash(__name__)
server = app.server
app.title = "Tournament Dashboard"

#build out any static graphs up here and then drop them into app.layout below
factionOptions=[{'label':'All','value':'all'},
            {'label':'Rebel','value':'rebel'},
            {'label':'Imperial','value':'imperial'},
            {'label':'Republic','value':'republic'},
            {'label':'Separatist','value':'separatist'}]
############## FACTION COUNT PIE CHART ##############
labels = [faction['name'] for faction in summaryStats['factions']]
values = [faction['count'] for faction in summaryStats['factions']]
factionFig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'textinfo': 'value',
            'marker': {'colors':[colors[label] for label in labels]}}]}

#################################################################
############################ THE APP ############################
#################################################################
app.layout = html.Div([
                dcc.Tabs(id='navigation', value='summary', children=[
                    dcc.Tab(label='Summary', value='summary', children=[
                        html.Div(className='row', children=[
                            html.Div(className='five columns', children=[
                                html.H2('Faction Count'),
                                dcc.Graph(figure=factionFig)]),
                            html.Div(className='five columns', children=[
                                html.H2('Activation Count'),
                                dcc.Dropdown(id='activation-selection', value='all', options=factionOptions),
                                html.Div(id='activation-charts')])
                            ]),
                        html.Div(className='row', children=[
                            html.Div(className='five columns', children=[
                                html.H2('Rounds Played (coming soon)'),
                                dcc.Dropdown(id='rounds-selection', value='all', options=factionOptions)]),
                            html.Div(className='five columns', children=[
                                html.H2('Bids (coming soon)'),
                                dcc.Dropdown(id='bids-selection', value='all', options=factionOptions)])
                            ])
                    ]),
                    dcc.Tab(label='Factions', value='faction', children=[
                        dcc.Dropdown(id='faction-selection',
                            options=factionOptions),
                        html.H2('Rank Counts (coming soon)'),
                        html.H2('Points Spent on Rank (coming soon)'),
                        html.H2('Command Card Counts (coming soon)'), #does all of this stuff just belong with Summary?
                        html.H2('Battle Card Counts (coming soon)')
                    ]),
                    dcc.Tab(label='Units', value='units', children=[
                        dcc.Dropdown(id='unit-selection', className='eight columns',
                            options=[{'label':unit[1],'value':int(unit[0])} for unit in unitIDs],
                            value=int(unitIDs[0][0])),
                        html.Div(className='row', children=[
                            html.Div(id='graph', className='eight columns'),
                            html.Div(html.H6('Overall Win Rate')),
                            html.Div(html.H6('Rebel Win Rate')),
                            html.Div(html.H6('Imperial Win Rate')),
                            html.Div(html.H6('Republic Win Rate')),
                            html.Div(html.H6('Separatist Win Rate'))]),
                        #percent only? numbers might not make so much sense here...
                        html.Div(className='row', children=[
                            html.Div(className='two columns', children=[html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate'),
                                                                        html.H6('Objective Win Rate')]),
                            html.Div(className='two columns', children=[html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate'),
                                                                        html.H6('Condition Win Rate')]),
                            html.Div(className='two columns', children=[html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate'),
                                                                        html.H6('Deployment Win Rate')])
                            ])
                    ]),
                    dcc.Tab(label='Meta Lists',children=[
                        html.H2('Meta List drop down menu'),
                        html.H2('Meta List definitions (coming soon)'),
                        html.H2('Meta List counts (coming soon)'),
                        html.H2('Meta List Win Rates (coming soon)')
                    ])
                ]),
                html.Img(src=app.get_asset_url('BushFacts white.png'), width="303px", height="75px")
            ])

#######################################################################
############################ THE FUNCTIONS ############################
#######################################################################
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
            'x': labels,
            'y': values,
            'type': 'bar',
            'width': .5,
            'name': type.title()
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

@app.callback(
    Output('activation-charts','children'),
    [Input('activation-selection','value')])
def update_activation_chart(faction):
    #make a static min/max x range for persepctive
    xmin = min([act['act'] for act in summaryStats['activations']['all']])
    xmax = max([act['act'] for act in summaryStats['activations']['all']])
    labels = [str(act['act']) for act in summaryStats['activations'][faction]]
    values = [act['count'] for act in summaryStats['activations'][faction]]
    activationFig = {'data': [{'x': labels, 'y': values, 'width': .5, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'name': 'activation'
                        }],
                    'layout':{
                        'xaxis1': {'range': [xmin-.5,xmax+.5], 'autorange': False, 'dtick': 1}
                        }
                    }
    return dcc.Graph(figure=activationFig)


if __name__ == '__main__':
    app.run_server(debug=True)
