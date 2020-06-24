#need bar widths to be relative to the screen, not number of categories...
#need to label the callbacks with something visible
#contents of all of app.layout can be moved to individual files
#maybe keep callback instance here, but the functions they reference can even go to other files


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

eventOptions = [{'label': 'IL5 Round Robin', 'value': 133},
                {'label': 'IL5 Single Elimination', 'value': 134}]

battleCardNames = json.loads(open("data/battleCardNames.json").read())

colors = {'rebel':'#A91515', 'imperial':'#6B6B6B', 'republic':'#C49D36', 'separatist':'#101A48',
            'heavy weapon':'#1F37CD', 'personnel':'#1F77B4', 'force':'#FF7F0E', 'command':'#D62728', 'hardpoint':'#D62728',
            'gear':'#2CA02C', 'grenades':'#BA57A9', 'comms':'#552923', 'pilot':'#FF7F0E', 'training':'#731FCD',
            'generator':'#7F7F7F', 'armament':'#7CD6DF', 'crew':'#2CA02C', 'ordnance':'#1F77B4', 'counterpart':'#FF7F0E'
            }
defaultColors = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd','#8c564b','#e377c2','#7f7f7f','#bcbd22','#17becf']
battleColors = {}
for battleType in ['objectives', 'conditions','deployments']:
    j = 0
    for i in battleCardNames[battleType]:
        battleColors[i] = defaultColors[j]
        j += 1
        if j == 10: j=0;
factionShades = {'rebel': ['#A91515','#891212','#651616'], 'imperial': ['#6B6B6B','#5A5959','#454343','#333333'],
                'republic': ['#C49D36','#A27F0D'], 'separatist': ['#101A48','#162A87','#1942FF']}

app = dash.Dash(__name__)
server = app.server
app.title = "Tournament Dashboard"

#build out any static graphs up here and then drop them into app.layout below
factionOptions=[{'label':'All','value':'all'},
            {'label':'Rebel','value':'rebel'},
            {'label':'Imperial','value':'imperial'},
            {'label':'Republic','value':'republic'},
            {'label':'Separatist','value':'separatist'}]

##################################################################
############################ THE SITE ############################
##################################################################
app.layout = html.Div([
                html.Div(className='row', children=[
                    html.Div(className='two columns', children=[
                        html.H6('Choose an event:')
                    ]),
                    html.Div(className='three columns', children=[
                        dcc.Dropdown(id='event-selection', value=133, options=eventOptions)
                    ]),
                    # DATA CACHE
                    html.Div(id='unit-data', style={'display': 'none'}),
                    html.Div(id='summary-data', style={'display': 'none'}),
                    html.Div(id='list-data', style={'display': 'none'}),
                    html.Div(id='meta-data', style={'display': 'none'}),
                    html.Div(id='unitID-data', style={'display': 'none'}),
                    html.Div(id='faction-rate-data', style={'display': 'none'}),
                    html.Div(id='win-rate-data', style={'display': 'none'})
                ]),
                dcc.Tabs(id='navigation', value='units', children=
                    [
                    dcc.Tab(label='Summary', value='summary', children=
                        [
                        html.Div(className='row', children=
                            [
                            html.Div(className='five columns', children=
                                [
                                html.H2('Faction Count'),
                                html.Div(id='faction-chart')
                                ]
                            ),
                            html.Div(className='five columns', children=
                                [
                                html.H2('Activation Count'),
                                dcc.Dropdown(id='activation-selection', value='all', options=factionOptions),
                                html.Div(id='activation-charts'),
                                html.Div(id='activation-average')
                                ]
                            )]
                        ),
                        html.Div(className='row', children=
                            [
                            html.Div(className='five columns', children=
                                [
                                html.H2('Rounds Played (coming soon)'),
                                dcc.Dropdown(id='rounds-selection', value='all', options=factionOptions)
                                ]
                            ),
                            html.Div(className='seven columns', children=
                                [
                                html.H2('Bid Counts'),
                                dcc.Dropdown(id='bid-selection', value='all', options=factionOptions),
                                html.Div(id='bid-charts'),
                                html.Div(id='bid-average')
                                ]
                            )]
                        )]
                    ),
                    dcc.Tab(label='Ranks', value='rank', children=
                        [
                        dcc.Dropdown(id='rank-selection', value='all', options=factionOptions),
                        html.Div(id='rank-pages')
                        ]
                    ),
                    dcc.Tab(label='Units', value='units', children=
                        [
                        dcc.Dropdown(id='unit-selection', className='eight columns'
                            # options=[{'label':unit[1],'value':int(unit[0])} for unit in unitIDs],
                            ),
                        html.Div(className='row', children=
                            [
                            html.Div(id='graph', className='eight columns'),
                            html.Div(html.H6('Overall Win Rate')),
                            html.Div(id='unit-faction-rates'),
                            html.Div(html.H6('Rebel Win Rate')),
                            html.Div(html.H6('Imperial Win Rate')),
                            html.Div(html.H6('Republic Win Rate')),
                            html.Div(html.H6('Separatist Win Rate'))
                            ]
                        ),
                        #percent only? numbers might not make so much sense here...
                        html.Div(className='row', children=
                            [
                            html.Div(className='two columns', children=
                                [
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate'),
                                html.H6('Objective Win Rate')
                                ]
                            ),
                            html.Div(className='two columns', children=
                                [
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate'),
                                html.H6('Condition Win Rate')
                                ]
                            ),
                            html.Div(className='two columns', children=
                                [
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate'),
                                html.H6('Deployment Win Rate')
                                ]
                            )]
                        )]
                    ),
                    dcc.Tab(label='Commands', value='commands', disabled=False, children=
                        [
                        html.Div(className='six columns offset-by-three columns', children=
                            [
                            dcc.Dropdown(id='command-selection', options=factionOptions, value='all'),
                            html.H2("1 pips"),
                            html.Div(id='command1-charts')
                            ]
                        ),
                        html.Div(className='row', children=
                            [
                            html.Div(className='six columns', children=
                                [
                                html.H2("2 pips"),
                                html.Div(id='command2-charts')
                                ]
                            ),
                            html.Div(className='six columns', children=
                                [
                                html.H2("3 pips"),
                                html.Div(id='command3-charts')
                                ]
                            )]
                        )]
                    ),
                    dcc.Tab(label='Battles', value='battles', disabled=False, children=
                        [
                        html.Div(className='six columns offset-by-three columns', children=
                            [
                            dcc.Dropdown(id='battle-selection', options=factionOptions, value='all'),
                            html.H2("Objectives"),
                            html.Div(id='objective-charts')
                            ]
                        ),
                        html.Div(className='row', children=
                            [
                            html.Div(className='six columns', children=
                                [
                                html.H2("Conditions"),
                                html.Div(id='condition-charts')
                                ]
                            ),
                            html.Div(className='six columns', children=
                                [
                                html.H2("Deployments"),
                                html.Div(id='deployment-charts')
                                ]
                            )]
                        )]
                    ),
                    dcc.Tab(label='Meta Lists', value='meta', children=
                        [
                        dcc.Dropdown(id='meta-selection', value='summary'),
                            # [{'label':'Summary', 'value':'summary'},{'label':'Comparison','value':'comparison'},
                            # {'label':'Meta List 1','value':'meta1'},{'label':'Meta List 2','value':'meta2'},
                            # {'label':'Meta List 3','value':'meta3'}]),
                        html.Div(id='meta-pages'),
                        html.Div(id='meta-summary-chart', style={'display': 'none'})
                        ]
                    )]
                ),
                html.Img(src=app.get_asset_url('BushFacts white.png'), width="303px", height="75px")
            ])
#######################################################################
############################### THE DATA ##############################
#######################################################################
@app.callback(
    Output('unit-data', 'children'),
    [Input('event-selection', 'value')])
def update_unit_data(event):
    unitStats = json.loads(open("data/"+str(event)+"/unitStats.json").read())
    return unitStats

@app.callback(
    Output('summary-data', 'children'),
    [Input('event-selection', 'value')])
def update_summary_data(event):
    stats = json.loads(open("data/"+str(event)+"/summaryStats.json").read())
    return stats

@app.callback(
    Output('list-data', 'children'),
    [Input('event-selection', 'value')])
def update_list_data(event):
    stats = json.loads(open("data/"+str(event)+"/listStats.json").read())
    return stats

@app.callback(
    Output('meta-data', 'children'),
    [Input('event-selection', 'value')])
def update_meta_data(event):
    stats = json.loads(open("data/"+str(event)+"/metaListStats.json").read())
    return stats

@app.callback(
    Output('faction-rate-data', 'children'),
    [Input('event-selection', 'value')])
def update_faction_rate_data(event):
    stats = json.loads(open("data/"+str(event)+"/factionWinRateStats.json").read())
    return stats

@app.callback(
    Output('win-rate-data', 'children'),
    [Input('event-selection', 'value')])
def update_win_rate_data(event):
    stats = json.loads(open("data/"+str(event)+"/winRateStats.json").read())
    return stats

@app.callback(
    Output('unitID-data', 'children'),
    [Input('unit-data', 'children')])
def update_unitID_data(unitStats):
    unitIDs = [[unit,unitStats[unit]['name']] for unit in unitStats]
    unitIDs.sort(key=lambda x:x[1])
    return unitIDs


#######################################################################
############################ THE FUNCTIONS ############################
#######################################################################
@app.callback(
    [Output('unit-selection', 'options'),
    Output('unit-selection', 'value')],
    [Input('unitID-data', 'children')])
def update_unit_dropdown(data):
    unitIDs = data
    options=[{'label':unit[1],'value':int(unit[0])} for unit in unitIDs]
    value = 46
    return options, value

@app.callback(
    Output('faction-chart', 'children'),
    [Input('summary-data', 'children')])
def update_faction_pie_chart(data):
    summaryStats = data
    labels = [faction['name'] for faction in summaryStats['factions']]
    values = [faction['count'] for faction in summaryStats['factions']]
    factionFig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'textinfo': 'value',
                'marker': {'colors':[colors[label] for label in labels]}}]}
    return dcc.Graph(figure=factionFig)

@app.callback(
    [Output('graph', 'children'),
    Output('unit-faction-rates', 'children')],
    [Input('unit-selection', 'value'),
    Input('unit-data','children'),
    Input('unitID-data','children'),
    Input('win-rate-data','children')])
def update_figure(select, data, ids, data2):
    unitStats = data
    unitIDs = ids
    winRateStats = data2

    traces = []
    unitID = str(select)
    unitName = unitStats[unitID]['name']
    unitCount = int(unitStats[unitID]['count'])
    unitRank =  unitStats[unitID]['rank']
    graphColors = []
    for type in unitStats[unitID]['upgrades']:
        data = [{'name':upgrade, 'count':int(unitStats[unitID]['upgrades'][type][upgrade])} for upgrade in unitStats[unitID]['upgrades'][type]]
        #sort before graphing
        data.sort(reverse=True, key=lambda x:x['count'])
        labels = [upgrade['name'] for upgrade in data]
        values = [upgrade['count'] for upgrade in data]
        graphColors.append(colors[type])
        traces.append({
            'x': labels,
            'y': values,
            'type': 'bar',
            'width': .5,
            'name': type.title(),
            'marker': {'color': colors[type]}
        })
    factionPieCharts = {}
    for faction in winRateStats[str(select)]['factions']:
        values = [winRateStats[str(select)]['factions'][faction]["wins"],winRateStats[str(select)]['factions'][faction]["games"]-winRateStats[str(select)]['factions'][faction]["wins"]]
        labels = ["wins", "losses"]
        factionFig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'textinfo': 'value',
                    'marker': {'colors':[colors[faction],"#ffffff"]}}]}
        factionPieCharts[faction] = factionFig
    return html.Div(dcc.Graph(id='test',
        figure={
            'data': traces,
            'layout': {
                'yaxis': {'range': [0,unitCount]},
                'transition': {'duration': 500},
                'title': unitName + "<br>" + str(unitCount) + " in attendance"
            }
        })), html.Div(dcc.Graph(figure=factionPieCharts['republic']))

@app.callback(
    [Output('activation-charts','children'),
    Output('activation-average','children')],
    [Input('activation-selection','value'),
    Input('summary-data','children')])
def update_activation_chart(faction, data):
    summaryStats = data
    #make a static min/max x range for persepctive
    xmin = min([act['act'] for act in summaryStats['activations']['all']])
    xmax = max([act['act'] for act in summaryStats['activations']['all']])
    labels = [act['act'] for act in summaryStats['activations'][faction]]
    values = [act['count'] for act in summaryStats['activations'][faction]]
    average = sum([labels[i]*values[i] for i in range(len(values))])/sum(values)
    activationFig = {'data': [{'x': labels, 'y': values, 'width': .5, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'name': 'activation'
                        }],
                    'layout':{
                        'xaxis1': {'range': [xmin-.5,xmax+.5], 'autorange': False, 'dtick': 1}
                        }
                    }
    return dcc.Graph(figure=activationFig), html.H6('Activation Average: ' + str('%.2f'%(average)))

@app.callback(
    [Output('bid-charts','children'),
    Output('bid-average','children')],
    [Input('bid-selection','value'),
    Input('summary-data','children')])
def update_bid_chart(faction, data):
    summaryStats = data
    #make a static min/max x range for persepctive
    xmin = min([bid['bid'] for bid in summaryStats['bids']['all']])
    xmax = max([bid['bid'] for bid in summaryStats['bids']['all']])
    labels = [bid['bid'] for bid in summaryStats['bids'][faction]]
    values = [bid['count'] for bid in summaryStats['bids'][faction]]
    average = sum([labels[i]*values[i] for i in range(len(values))])/sum(values)
    #reformat to strings? maybe?
    # labels = [str(bid['bid']) for bid in summaryStats['bids'][faction]]
    bidFig = {
            'data': [{'x': labels, 'y': values, 'width': .6, 'textinfo': 'value', 'type': 'bar',
                'textinfo': 'value', 'name': 'bid', 'marker':{'color':defaultColors[2]}}],
            'layout':{'xaxis1': {'range': [xmin-.5,xmax+.5], 'autorange': False, 'dtick': 1}}
            }
    return dcc.Graph(figure=bidFig), html.H6('Bid Average: ' + str('%.2f'%(average)))

@app.callback(
    [Output('command1-charts','children'),
    Output('command2-charts','children'),
    Output('command3-charts','children')],
    [Input('command-selection','value'),
    Input('summary-data','children')]
)
def update_command_chart(faction, data):
    summaryStats = data
    commandCharts = {}
    commandColors = [defaultColors[3],defaultColors[4],defaultColors[2]]
    for i in range(1,4):
        #sort before graphing
        data = [{'name': command['name'],'count':command['count']} for command in summaryStats['commands'][faction][str(i)]]
        data.sort(reverse=True, key=lambda x:x['count'])
        labels = [command['name'] for command in data]
        values = [command['count'] for command in data]
        commandCharts[i] = {
                            'data': [{'x': labels, 'y': values, 'width': .5, 'textinfo': 'value', 'type': 'bar',
                                'textinfo': 'value', 'name': str(i)+'-pips', 'marker':{'color':commandColors[i-1]}}],
                            'layout': {'autosize': True, 'margin': {'t':20, 'r':20}}
                            }
    return dcc.Graph(figure=commandCharts[1]),dcc.Graph(figure=commandCharts[2]),dcc.Graph(figure=commandCharts[3])

@app.callback(
    [Output('objective-charts','children'),
    Output('condition-charts','children'),
    Output('deployment-charts','children')],
    [Input('battle-selection','value'),
    Input('summary-data','children')]
)
def update_battle_chart(faction, data):
    summaryStats = data
    battleCharts = {}
    for i in ['objectives','conditions','deployments']:
        #sort before graphing
        data = [{'name': battle['name'],'count':battle['count']} for battle in summaryStats['battles'][faction][i]]
        # data.sort(reverse=True, key=lambda x:x['count'])

        labels = [battle['name'] for battle in data]
        values = [battle['count'] for battle in data]
        battleCharts[i] = {
                            'data': [{'labels': labels, 'values': values, 'textinfo': 'value', 'type': 'pie',
                            'marker': {'colors':[battleColors[label] for label in labels]}}],
                            }
    return dcc.Graph(figure=battleCharts['objectives']),dcc.Graph(figure=battleCharts['conditions']),dcc.Graph(figure=battleCharts['deployments'])

@app.callback(
    Output('meta-selection', 'options'),
    [Input('meta-data', 'children')])
def update_meta_dropdown(data):
    metaListStats = data
    metaOptions=[{'label':'Summary','value':'summary'},{'label':'Comparison','value':'comparison'}]
    for faction in metaListStats:
        index = 0
        for meta in metaListStats[faction]:
            if meta['count'] > 0:
                metaOptions += [{'label':"--" + meta['name'], 'value': faction+"~"+str(index)}]
            index += 1
    return metaOptions

@app.callback(
    Output('meta-summary-chart', 'children'),
    [Input('meta-data', 'children')])
def update_meta_summary_chart(data):
    metaListStats = data

    labels = []
    values = []
    c = []
    for faction in metaListStats:
        labels = labels + [meta["name"] for meta in metaListStats[faction]]
        values = values + [meta["count"] for meta in metaListStats[faction]]
        c = c + factionShades[faction]
    labels += ["Off-Meta"]
    values += [metaListStats["rebel"][0]["off-meta total"]]
    c += ["#F0F0F0"]
    metaSummaryFig = {'data': [{'labels': labels, 'values': values, 'type': 'pie', 'textinfo': 'value',
                'marker': {'colors': c}}]}
    return metaSummaryFig

@app.callback(
    Output('meta-pages','children'),
    [Input('meta-selection','value'),
    Input('meta-summary-chart','children'),
    Input('meta-data','children')]
)
def update_meta_pages(page, metaSummaryFig, data):
    content = ''
    metaListStats = data
    if page == 'summary':
        content = html.Div(className="five columns", children=[
            html.H2('division of which lists were meta lists and which were not'),
            dcc.Graph(figure=metaSummaryFig)
            ])
    elif page == 'comparison':
        content = html.H2('n^2-n pie charts of each meta list playing against each other')
    else:
        faction = page.split('~')[0]
        metaNumber = page.split('~')[1]
        units = metaListStats[faction][int(metaNumber)]["units"]
        units.sort(reverse=True, key=lambda x:x['count'])
        labels = [unit["name"] for unit in units]
        values = [unit["count"] for unit in units]
        metaUnitChart = {'data': [{'x':labels, 'y':values, 'type':'bar'}]}
        upgrades = metaListStats[faction][int(metaNumber)]["upgrades"]
        upgrades.sort(reverse=True, key=lambda x:x['count'])
        labels = [upgrade["name"] for upgrade in upgrades]
        values = [upgrade["count"] for upgrade in upgrades]
        metaUpgradeChart = {'data': [{'x':labels, 'y':values, 'type':'bar'}]}

        content = html.Div([
            html.H1(metaListStats[faction][int(metaNumber)]["name"]),
            html.H3("count: " + str(metaListStats[faction][int(metaNumber)]["count"])),
            html.H4("requirements: " + metaListStats[faction][int(metaNumber)]["img"]),
            html.H4('central picture of the cards required to be considered this meta list'),
            html.Div(className="row", children=[
                html.Div(className="six columns", children=[dcc.Graph(figure=metaUnitChart)]),
                html.Div(className="six columns", children=[dcc.Graph(figure=metaUpgradeChart)])
                ]),
            html.H4('win rates v each faction'),
            html.H4('win rates with each battle selection'),
            html.H4('battle card association'),
            html.H4('bid association'),
            html.H4('activation count association')
            ])
    return content

@app.callback(
    Output('rank-pages','children'),
    [Input('rank-selection','value'),
    Input('unit-data', 'children'),
    Input('unitID-data', 'children')]
)
def update_rank_pages(selection, data, ids):
    unitStats = data
    unitIDs = ids
    #id, name, rank, count, faction limited to this faction
    if selection == 'all':
        rankData = [[unit[0],unit[1],unitStats[unit[0]]['rank'],unitStats[unit[0]]['count'],unitStats[unit[0]]['faction']] for unit in unitIDs]
    else:
        rankData = [[unit[0],unit[1],unitStats[unit[0]]['rank'],unitStats[unit[0]]['count'],unitStats[unit[0]]['faction']] for unit in unitIDs if unitStats[unit[0]]['faction']==selection]
    rankData.sort(reverse=True, key=lambda x:x[3])
    heroData = [unit for unit in rankData if unit[2] in ['commander','operative']]
    labels = [unit[1] for unit in heroData]
    values = [unit[3] for unit in heroData]
    theseColors = [colors[unit[4]] for unit in heroData]
    heroFig =   {
                'data': [{'x': labels, 'y': values, 'width': .6, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'marker':{'color':theseColors}}],
                'layout': {'autosize': True}
                }
    corpsData = [unit for unit in rankData if unit[2] == 'corps']
    labels = [unit[1] for unit in corpsData]
    values = [unit[3] for unit in corpsData]
    theseColors = [colors[unit[4]] for unit in corpsData]
    corpsFig =   {
                'data': [{'x': labels, 'y': values, 'width': .6, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'marker':{'color':theseColors}}],
                'layout': {'autosize': True}
                }
    sfData = [unit for unit in rankData if unit[2] == 'special']
    labels = [unit[1] for unit in sfData]
    values = [unit[3] for unit in sfData]
    theseColors = [colors[unit[4]] for unit in sfData]
    sfFig =   {
                'data': [{'x': labels, 'y': values, 'width': .6, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'marker':{'color':theseColors}}],
                'layout': {'autosize': True}
                }
    vehicleData = [unit for unit in rankData if unit[2] in ['heavy','support']]
    labels = [unit[1] for unit in vehicleData]
    values = [unit[3] for unit in vehicleData]
    theseColors = [colors[unit[4]] for unit in vehicleData]
    vehicleFig =   {
                'data': [{'x': labels, 'y': values, 'width': .6, 'textinfo': 'value', 'type': 'bar',
                    'textinfo': 'value', 'marker':{'color':theseColors}}],
                'layout': {'autosize': True}
                }

    content = html.Div(children=[
        html.Div(className='row', children=
            [
            html.Div(className='six columns', children=[
                html.H2('points spent on each rank, pie chart')
                ]),
            html.Div(className='six columns', children=[
                html.H2('commanders and operatives'),
                dcc.Graph(figure=heroFig)
                ])
            ]),
        html.Div(className='row', children=
            [
            html.Div(className='four columns', children=[
                html.H5('corps'),
                dcc.Graph(figure=corpsFig)
                ]),
            html.Div(className='four columns', children=[
                html.H5('special forces. bleh. maybe show the heavies here?'),
                dcc.Graph(figure=sfFig)
                ]),
            html.Div(className='four columns', children=[
                html.H5('support and heavy'),
                dcc.Graph(figure=vehicleFig)
                ])
            ])])
    return content







if __name__ == '__main__':
    app.run_server(debug=True)
