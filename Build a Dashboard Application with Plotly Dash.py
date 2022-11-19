# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv')
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
# spacex_df.columns

site_list = [i for i in spacex_df['Launch Site'].unique()]

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                html.Div(dcc.Dropdown(id='input-site',
                                                        options=[{'label': 'All Sites', 'value': 'ALL'}]
                                                        + [{'label': i, 'value': i} for i in site_list],
                                                        value='ALL',
                                                        placeholder="All Sites",
                                                        searchable=True
                                                        ),),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-range-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    2500: '2500',
                                                    5000: '5000',
                                                    7500: '7500',
                                                    10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ]
                        )

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(  [Output(component_id='success-pie-chart', component_property='figure'),
                 Output(component_id='success-payload-scatter-chart', component_property='figure')
                ],
                [Input(component_id='input-site', component_property='value'),
                 Input(component_id="payload-range-slider", component_property="value")
                ]
)
               #Holding output state till user enters all the form information. In this case, it will be chart type and year

def get_graph(site, payload_range):
    
    if site == 'ALL':
        success_pie_chart_fig = px.pie(spacex_df, names = 'class', title='Success of All Sites')
        success_payload_scatter_chart_fig = px.scatter(spacex_df[(spacex_df['Payload Mass (kg)']>=payload_range[0]) & (spacex_df['Payload Mass (kg)']<=payload_range[1])], x = 'Payload Mass (kg)', y = 'class', color='Booster Version Category')

    else:
        success_pie_chart_fig = px.pie(spacex_df[spacex_df['Launch Site']==site], names = 'class', title = 'Success at ' + site)
        success_payload_scatter_chart_fig = px.scatter(spacex_df[(spacex_df['Launch Site']==site) & (spacex_df['Payload Mass (kg)']>=payload_range[0]) & (spacex_df['Payload Mass (kg)']<=payload_range[1])], x = 'Payload Mass (kg)', y = 'class', color='Booster Version Category')

    return  [success_pie_chart_fig, success_payload_scatter_chart_fig]
            
# Run the app
if __name__ == '__main__':
    app.run_server()
