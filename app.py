import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
unitIDs = pd.read_csv('data/units/counts.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    dcc.Graph(id='graph-with-dropdown'),
    dcc.Dropdown(
                id='unit-name',
                options=[{'label': unitIDs["name"][i], 'value': i} for i in range(len(unitIDs))],
                value=43
            )
])

@app.callback(
    Output('graph-with-dropdown', 'figure'),
    [Input('unit-name', 'value')])
def update_figure(selected_df_ID):
    selected_unitID = unitIDs.at[selected_df_ID,'id']
    unitName = unitIDs.at[selected_df_ID,'name']
    unitCount = unitIDs.at[selected_df_ID,'count']
    df = pd.read_csv('data/units/upgrades/' + str(selected_unitID) + ".csv")
    data = [{'values': [i for i in df['count']], 'labels': [i for i in df['upgrades']], 'type': 'pie', 'title': unitName + ": " + str(unitCount) + "\n"}]
    fig = go.Figure()
    return {
        "data": data
    }


if __name__ == '__main__':
    app.run_server(debug=True)
