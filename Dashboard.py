# # Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'site1', 'value': 'site1'},
                                ],
                                value='ALL',
                                placeholder='Select a Launch Site here',
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                    
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                # dcc.RangeSlider(id='payload-slider',
                                # min=0, max=10000, step=1000,
                                # marks={0: '0',100: '100'}, 
                                # value=[min_payload, max_payload],
                                # marks={int(min_payload): str(int(min_payload)),
                                # int(max_payload): str(int(max_payload))}),
                                dcc.RangeSlider(
                                    id='payload-slider',
                                    min=min_payload,
                                    max=max_payload,
                                    step=1000,
                                    value=[min_payload, max_payload],
                                    marks={int(min_payload): str(int(min_payload)),
                                    int(max_payload): str(int(max_payload))}
    ),


                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# @app.callback(Output(component_id='success-pie-chart',component_property='figure'),
#                                 Input(component_id='site-dropdown',component_property='value'))
#                                 def get_pie_chart(entered_site):
#                                     filtered_df=spacex_df
#                                     if entered_site=='ALL':
#                                         fig=px.pie(filtered_df,values='class',
#                                         names='pie chart names',
#                                         title='title')
#                                         return fig
#                                     else:
#                                         # Filter records for the selected launch site
#                                         site_df = filtered_df[filtered_df['Launch Site'] == entered_site]
#                                         fig=px.pie(
#                                             site_df,
#                                             names='class',
#                                             title=f'Success Vs Failure for site{entered_site}'
#                                         )
#                                         return fig

# Function decorator to specify function input and output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    # Use the original dataframe
    filtered_df = spacex_df

    # Case 1: All sites selected
    if entered_site == 'ALL':
        fig = px.pie(
            filtered_df,
            values='class',                  # class = 1 (success), so sum gives total successes
            names='Launch Site',             # pie slices for each site
            title='Total Successful Launches by Site'
        )
        return fig

    # Case 2: Specific site selected
    else:
        # Filter records for the selected launch site
        site_df = filtered_df[filtered_df['Launch Site'] == entered_site]

        # Show success vs failure counts for that site
        fig = px.pie(
            site_df,
            names='class',                   # 0 = fail, 1 = success
            title=f'Success vs Failure for site {entered_site}'
        )
        return fig
     
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
Input(component_id='site-dropdown',component_property='value'))
def get_scatter_chart(entered_site,payload_range):
    low,high=payload_range
    df_filtered=spacex_df[
        (spacex_df['Payload Mass (kg)']>=low) &
        (spacex_df['Payload Mass (kg)']<=high)
    ]
    # if entered_site=='ALL':
    #     fig=px.scatter(df_filtered,
    #     values='class',
    #     names='scatter chart names',
    #     title='title'
    #     =
    #     return fig
    # Case 1: All sites selected
    if entered_site == 'ALL':
        fig = px.scatter(
            df_filtered,
            values='class',                  # class = 1 (success), so sum gives total successes
            names='Launch Site',             # pie slices for each site
            title='Total Successful Launches by Site'
        )
        return fig

    else:
        df_filtered = df_filtered[df_filtered['Launch Site'] == selected_site]
        fig = px.scatter(
        df_filtered,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success'
    )
    return fig

# Run the app
if __name__ == '__main__':
    app.run()
