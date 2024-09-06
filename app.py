import os
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px


# Initialize the Dash app with suppressed callback exceptions
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Dashboard Layout"

server = app.server

# URL of the Excel file on GitHub
url1 = 'https://github.com/dogitosanchez/livrable/raw/main/aGLP1_english.xlsx'
url2 = 'https://github.com/dogitosanchez/livrable/raw/main/Insuline_anglais.xlsx'

# Load the specific sheet 'Complet' from each file
cleaned_data = pd.read_excel(url1, sheet_name='Complet')
cleaned_data2 = pd.read_excel(url2, sheet_name='Complet')

# Print a specific column, e.g., 'Collection Mode'
print(cleaned_data['Collection Mode'])

# Ensure 'Year' column is created
cleaned_data['Year'] = pd.to_datetime(cleaned_data['Notif'], dayfirst=True).dt.year
cleaned_data2['Year'] = pd.to_datetime(cleaned_data2['Notif'], dayfirst=True).dt.year

# Function to generate the interactive Plotly line graph for Insulin data
def create_plotly_insulin_line_graph():
    # Count the number of cases per year for insulin data
    insulin_year_count = cleaned_data2['Year'].value_counts().sort_index()

    # Create the Plotly figure
    fig = px.line(insulin_year_count, x=insulin_year_count.index, y=insulin_year_count.values, markers=True, 
                  labels={'x': 'Year', 'y': 'Number of cases'},
                  title='Number of Insulin cases per year')

    fig.update_traces(marker=dict(size=10, color='lightcoral'), line=dict(color='lightcoral'))

    # Update hover label properties
    fig.update_traces(hoverlabel=dict(bgcolor="coral", font_size=16, font_family="Arial"))

    fig.update_layout(
        xaxis_title='Year', 
        yaxis_title='Number of cases', 
        xaxis=dict(range=[2004, 2024]),  # Set x-axis range
        title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        height=500, 
        autosize=True
    )  # Adjust height and width

    return fig

# Function to generate the interactive Plotly line graph
def create_plotly_line_graph():
    # Count the number of cases per year
    filtered_data = cleaned_data.copy()
    year_count = filtered_data['Year'].value_counts().sort_index()
    # Create the Plotly figure
    fig = px.line(year_count, x=year_count.index, y=year_count.values, markers=True, 
                  labels={'x': 'Year', 'y': 'Number of cases'},
                  title='Number of cases per year')

    fig.update_traces(marker=dict(size=10, color='coral'), line=dict(color='lightcoral'))

    # Update hover label properties
    fig.update_traces(hoverlabel=dict(bgcolor="coral", font_size=16, font_family="Arial"))

    fig.update_layout(xaxis_title='Year', yaxis_title='Number of cases', xaxis=dict(range=[2004, 2024]),
                      title={'x':0.5, 'xanchor': 'center'},  # Center the title
                      height=500, autosize=True)  # Adjust height and width

    return fig


# Function to generate the interactive Plotly histogram for Insulin data (by Collection Method)
def create_plotly_insulin_histogram():
    # Create the Plotly figure for the histogram
    fig = px.histogram(cleaned_data2, 
                       x='Collection Method', 
                       color='Collection Method',  # Use the 'Collection Method' for coloring
                       labels={'x': 'Method of collection', 'y': 'Number of cases'},
                       title='Distribution of medication errors by method of collection')

    # Update the layout of the chart
    fig.update_layout(xaxis_title='Method of collection', 
                      yaxis_title='Number of cases', 
                      title={'x': 0.5, 'xanchor': 'center'},  # Center the title
                      height=500, width=600,  # Adjust height and width
                      xaxis=dict(tickangle=-30))  # Tilt the x-axis labels

    return fig


# Function to generate the interactive Plotly histogram
def create_plotly_histogram():
    # Create the Plotly fiagure
    fig = px.histogram(cleaned_data, x='Collection Mode', color='Collection Mode',
                       labels={'Collection Mode': 'Method of collection', 'count': 'Number of cases'},
                       title='Distribution of medication errors by method of collection')

    fig.update_layout(
        xaxis_title='Method of collection', 
        yaxis_title='Number of cases', 
        title={'x':0.5, 'xanchor': 'center'},  # Center the title
        height=500, width=600,  # Adjust height and width
        xaxis=dict(tickangle=-30)  # Tilt x-axis labels
    )

    return fig

# Function to generate the interactive Plotly bar plot by Type of Case and Sex for Insulin data
def create_plotly_insulin_bar_by_sex():
    # Extract relevant columns and clean data
    insuline_data = cleaned_data2[['Sex', 'Typ Cas']].dropna()

    # Group data by 'Type of Case' and 'Sex'
    category_sex_counts = insuline_data.groupby(['Typ Cas', 'Sex']).size().unstack()

    # Create a Plotly bar chart with custom colors
    fig = px.bar(category_sex_counts, 
                 x=category_sex_counts.index, 
                 y=[category_sex_counts['F'], category_sex_counts['M']], 
                 labels={'value': 'Number of incidents', 'Typ Cas': 'Typ Cas'},
                 title='Incidents per Type of Case and Sex')

    # Customize layout
    fig.update_layout(
        barmode='group',  # Set to group mode
        xaxis_title='Type of Case',
        yaxis_title='Number of incidents',
        title={'x': 0.5, 'xanchor': 'center'},  # Center the title
        height=500, width=600,  # Adjust height and width
        xaxis=dict(tickangle=-30)  # No rotation for x-axis labels
    )

    return fig

# Function to generate the interactive Plotly bar plot by Type of Case and Sex
def create_plotly_bar_plot():
    # Extract relevant columns and clean data
    agl_data = cleaned_data[['Sex', 'Type of Case']].dropna()

    # Group data by 'Typ Cas' and 'Sex'
    category_sex_counts = agl_data.groupby(['Type of Case', 'Sex']).size().unstack()

    # Create a Plotly bar chart
    fig = px.bar(category_sex_counts, x=category_sex_counts.index, y=[category_sex_counts['F'], category_sex_counts['M']],
                 labels={'value': 'Number of incidents', 'Type of Case': 'Type of Case'},
                 title='Incidents per Type of Case and Sex')

    fig.update_layout(
        barmode='group',
        xaxis_title='Type of Case',
        yaxis_title='Number of incidents',
        title={'x':0.5, 'xanchor': 'center'},  # Center the title
        height=500, width=600,  # Adjust height and width
        xaxis=dict(tickangle=-30),  # Tilt x-axis labels
        legend_title_text="Sex"
    )

    return fig

# Function to create the Plotly graph for the distribution of medication errors by declaration type and year
def create_plotly_insulin_declaration_graph():
    # Ensure 'Year' column is created
    cleaned_data2['Year'] = pd.to_datetime(cleaned_data2['Notif'], dayfirst=True).dt.year
    # Handle missing values in 'Year' column by filling with 0 (or any placeholder)
    cleaned_data2['Year'] = cleaned_data2['Year'].fillna(0).astype(int)

    # Create a Plotly histogram plot similar to sns.countplot
    fig = px.histogram(
        cleaned_data2,
        x='Year',
        color='Declaration Type',
        labels={'x': 'Year', 'y': 'Number of cases'},
        title='Distribution of medication errors by type of declaration and by year',
        barmode='group'  # Use grouped bars like seaborn countplot
    )

    # Update layout and styling
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of cases',
        legend_title_text='Type of declaration',
        height=500, width=600,  # Adjusting size
        xaxis=dict(tickangle=0)  # Rotate x-axis labels if needed
    )

    return fig

def create_plotly_declaration_graph():
    # Ensure 'Year' column is created
    cleaned_data['Year'] = pd.to_datetime(cleaned_data['Notif'], dayfirst=True).dt.year
    # Handle missing values in 'Year' column by filling with 0 (or any placeholder)
    cleaned_data['Year'] = cleaned_data2['Year'].fillna(0).astype(int)

    # Create a Plotly histogram plot similar to sns.countplot
    fig = px.histogram(
        cleaned_data,
        x='Year',
        color='Declaration Type',
        labels={'x': 'Year', 'y': 'Number of cases'},
        title='Distribution of medication errors by type of declaration and by year',
        barmode='group'  # Use grouped bars like seaborn countplot
    )

    # Update layout and styling
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Number of cases',
        legend_title_text='Type of declaration',
        height=500, width=600,  # Adjusting size
        xaxis=dict(tickangle=0)  # Rotate x-axis labels if needed
    )

    return fig

# Function to create value boxes in a 2x2 grid layout
def create_value_boxes_insuline():
    return html.Div([
        # Row 1
        html.Div([
            # Box 1
            html.Div([
                html.H3("In this data base, male patients are significantly more likely to experience Dosage Errors (76.5%), highlighting a gender-specific trend.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'orange', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'}),
            
            # Box 2
            html.Div([
                html.H3("The 94.12% of Dosage Errors are severe, indicating that most Dosage Errors pose a high risk to patients.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'coral', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'gap': '20px'}),
        
        # Row 2
        html.Div([
            # Box 3
            html.Div([
                html.H3("Older patients (79 years on average) are more likely to experience Administration Errors without adverse effects, while younger patients (56 years) are more prone to Dosage Errors according to our pharmacovigilance database.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'lightblue', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'}),
            
            # Box 4
            html.Div([
                html.H3("Administration Errors peak during the winter (32.2%), suggesting a possible link between seasonality and error occurrence.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'lightgreen', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'gap': '20px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px', 'width': '100%', 'alignItems': 'center'})


# Function to create value boxes in a 2x2 grid layout
def create_value_boxes():
    return html.Div([
        # Row 1
        html.Div([
            # Box 1
            html.Div([
                html.H3("The mean age is significantly higher, at 68.78 ± 10.11 years, compared to 57.00 ± 9.54 years in Administration Errors without Adverse Effects. This suggests that in our database, older patients are more likely to experience dosage errors.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'lightblue', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'}),
            
            # Box 2
            html.Div([
                html.H3("For Dosage Errors, the mean weight is 95.86 ± 19.94 kg, and the corresponding BMI is 36.29 ± 9.46 kg/m². This highlights a pattern where heavier individuals are more prone to dosage errors.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'orange', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'gap': '20px'}),
        
        # Row 2
        html.Div([
            # Box 3
            html.Div([
                html.H3("Administration Errors : There is a higher percentage of females (63.2%) involved compared to males (36.8%) according to our pharmacovigilance database. Dosage Errors: The distribution is similar, with females representing 55.6% and males 44.4%.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'lightgreen', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'}),
            
            # Box 4
            html.Div([
                html.H3("The 47.37% of Administration Errors are classified as severe, compared to 77.78% of Dosage Errors. This highlights a higher risk level associated with dosage errors compared to general administration errors.", style={'color': 'white', 'margin': '10'}),
            ], style={'backgroundColor': 'coral', 'padding': '20px', 'borderRadius': '10px', 'width': '100%', 'textAlign': 'center'})
        ], style={'display': 'flex', 'justifyContent': 'space-between', 'width': '100%', 'gap': '20px'})
    ], style={'display': 'flex', 'flexDirection': 'column', 'gap': '20px', 'width': '100%', 'alignItems': 'center'})


# Layout of the app
app.layout = html.Div([
    # Top bar with image and title
    html.Div([
        html.Img(src='https://ilis.univ-lille.fr/_assets/cf96958808510cb4a29e461391f0eb9e/assets/img/logo-topbar.svg', 
                 style={'height': '30px', 'marginRight': '0px'}),
        html.H1(
            "Insulin/aGLP-1 autoinjectors and the difficulties encountered during injection as well as the adverse effects", 
            style={
                'display': 'inline-block', 
                'margin': '0', 
                'color': 'white', 
                'fontSize': '23px',  # Use clamp for responsive font size
                'textAlign': 'center',  # Center align text
                'flex': '1'# Take up remaining space for centering
            }),
    ], style={
        'backgroundColor': 'rgb(30, 26, 25)', 
        'padding': '30px', 
        'display': 'flex', 
        'alignItems': 'center', 
        'justifyContent': 'center',  # Center the contents horizontally
        'margin': '0', 
        'boxSizing': 'border-box'
    }),
    
    # Main content area with tabs and content
    html.Div([
        html.Div([
            dcc.Tabs(
                id="tabs", 
                value='tab-presentation', 
                vertical=True,
                children=[
                    dcc.Tab(
                        label='Overview', 
                        value='tab-presentation', 
                        style={
                            'backgroundColor': 'rgb(53, 53, 53)', 
                            'color': 'white', 
                            'textAlign': 'center',
                            'height': '40px',  
                            'lineHeight': '40px',
                            'width': '160px',  
                            'borderRadius': '8px',
                            'padding': '0px',  
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',  # Ensure no border is applied
                            'borderBottom': 'none',  # Explicitly remove any border-bottom
                            'fontSize': '20px'
                        }, 
                        selected_style={
                            'backgroundColor': 'rgb(0, 118, 186)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px',  
                            'lineHeight': '40px',
                            'width': '160px',
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',  # Ensure no border is applied
                            'borderBottom': 'none',  # Explicitly remove any border-bottom
                            'fontSize': '22px'
                        }
                    ),
                    dcc.Tab(
                        label='Insulin', 
                        value='tab-insuline', 
                        style={
                            'backgroundColor': 'rgb(53, 53, 53)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',  
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'fontSize': '20px'
                        }, 
                        selected_style={
                            'backgroundColor': 'rgb(0, 118, 186)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'fontSize': '22px'
                        }
                    ),
                    dcc.Tab(
                        label='aGLP-1', 
                        value='tab-aglp1', 
                        style={
                            'backgroundColor': 'rgb(53, 53, 53)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',  
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'fontSize': '20px'
                        }, 
                        selected_style={
                            'backgroundColor': 'rgb(0, 118, 186)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'fontSize': '22px'
                        }
                    ),
                    dcc.Tab(
                        label='About', 
                        value='tab-about', 
                        style={
                            'backgroundColor': 'rgb(53, 53, 53)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',  
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'borderBottom': 'none !important', # Force removal of border-bottom
                            'fontSize': '20px'
                        }, 
                        selected_style={
                            'backgroundColor': 'rgb(0, 118, 186)', 
                            'color': 'white', 
                            'textAlign': 'center', 
                            'height': '40px', 
                            'lineHeight': '40px',
                            'width': '160px',
                            'borderRadius': '8px',
                            'padding': '0px',
                            'margin': '10px auto',  
                            'boxSizing': 'border-box',
                            'border': 'none',
                            'borderBottom': 'none',  # Force removal of border-bottom
                            'fontSize': '22px'
                        }
                    ),
                ],
                style={'height': '100vh', 'borderRight': 'none', 'width': '100%'}
            ),
        ], style={
            'width': '15%', 
            'backgroundColor': 'rgb(53, 53, 53)', 
            'margin': '0', 
            'padding': '20px 0',  
            'display': 'flex', 
            'flexDirection': 'column', 
            'justifyContent': 'flex-start',  
            'alignItems': 'center',
            'border': 'none',
            'borderBottom': 'none'
        }),
        
        html.Div(id='tabs-content', 
                 style={'width': '85%', 'padding': '20px', 'margin': '0', 'backgroundColor': 'white', 'boxSizing': 'border-box'})
    ], style={'display': 'flex', 'margin': '0', 'padding': '0', 'height': '100%'})
])
            
from flask_caching import Cache

# Set up caching
cache = Cache(app.server, config={'CACHE_TYPE': 'SimpleCache', 'CACHE_DEFAULT_TIMEOUT': 300})

# Cache the line plot creation for aGLP-1
@cache.memoize()
def create_plotly_line_graph_cached():
    return create_plotly_line_graph()

# Cache the line plot creation for Insulin
@cache.memoize()
def create_plotly_insulin_line_graph_cached():
    return create_plotly_insulin_line_graph()

# In the callback or when rendering the aGLP-1 graph
agl_fig = create_plotly_line_graph_cached()

# In the callback or when rendering the insulin graph
insulin_fig = create_plotly_insulin_line_graph_cached()
# Callbacks to update the content based on the selected tab
@app.callback(
    Output('tabs-content', 'children'),
    Input('tabs', 'value')
)
def render_content(tab):
    if tab == 'tab-presentation':
        return html.Div([
            html.Img(
                src='https://www.diabeteswellness.no/media/wdcofqsq/injection-pen-with-needle.jpg?center=0.673146441088387,0.489979936985788&mode=crop&width=1200&height=630&rnd=133644018985000000', 
                style={'width': '100%', 'height': '400px', 'objectFit': 'cover', 'marginBottom': '50px'}  # Increase marginBottom to 30px
            ),  
            html.H2(
                'Project Overview',
                style={
                    'color': 'black', 
                    'fontSize': '30px',  # Text size
                    'textAlign': 'center',  # Center align text
                    'margin': '0',  # No margin around the text
                }
            ),
            html.H4('This project focuses on understanding the medication errors associated with aGLP-1 and insulin autoinjectors. With diabetes management being crucial to the well-being of millions, we explore how these errors occur and the impact they have on patients. Drawing from 16 years of data in the French national pharmacovigilance database, we aim to identify key trends, error types, and affected demographics. The findings shed light on the challenges patients and healthcare providers face, offering critical insights into improving both device use and patient safety.',
                style={
                    'color': 'black', 
                    'fontSize': '25px',  # Text size
                    'textAlign': 'justify',  # Justify text alignment for a professional look
                    'marginTop': '20px',  # Add margin to the top of the paragraph
                    'maxWidth': '1500px',  # Limit width to make text more readable
                    'marginLeft': 'auto',  # Center the block horizontally
                    'marginRight': 'auto',  # Center the block horizontally
                    'fontWeight': 'normal'  # Set the font weight to normal (not bold)
                }
            ),
            html.H4('Ultimately, the goal is to not only reduce the occurrence of these errors but also to guide the development of targeted educational programs and safety measures. By understanding where and why these issues arise, we can help ensure that patients receive the safest, most effective care possible, contributing to better health outcomes and enhanced quality of life for individuals using aGLP-1 and insulin therapies.',
                style={
                    'color': 'black', 
                    'fontSize': '25px',  # Text size
                    'textAlign': 'justify',  # Justify text alignment for a professional look
                    'marginTop': '20px',  # Add margin to the top of the paragraph
                    'maxWidth': '1500px',  # Limit width to make text more readable
                    'marginLeft': 'auto',  # Center the block horizontally
                    'marginRight': 'auto',  # Center the block horizontally
                    'fontWeight': 'normal'  # Set the font weight to normal (not bold)
                }
            )
        ], style={
            'textAlign': 'center',  # Center align the contents of the Div
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',  # Center align items horizontally
            'justifyContent': 'center',  # Center align items vertically
        })

    elif tab == 'tab-insuline':
        # Generate the interactive Plotly line graph for Insulin data
        insulin_line_fig = create_plotly_insulin_line_graph()
        # Generate the value boxes for Insulin data
        insulin_value_boxes = create_value_boxes_insuline()

        return html.Div([
            html.H3('Insulin Cases and Analysis'),
            html.Div([
                html.Div(dcc.Graph(figure=insulin_line_fig), style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
                html.Div(insulin_value_boxes, style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
            ], style={'display': 'flex', 'justifyContent': 'space-between'}),

            # Adding the dropdown selection bar for graph options
            html.Div([
                html.H5("Please select a graphic option that you want to visualize : ", style={'textAlign': 'left', 'marginBottom': '10px', 'fontSize' : '15px'}),
                dcc.Dropdown(
                id='insulin-graph-dropdown',
                options=[
                    {'label': 'Distribution of Medication Errors', 'value': 'histogram'},
                    {'label': 'Incidents per Type of Case', 'value': 'bar'},
                    {'label': 'Type of Declaration per Year', 'value': 'declaration'}
                ],
                value='histogram', 
                clearable=False,
                style={'width': '50%', 'marginLeft': '30px', 'paddingBottom': '10px'}
            ),

            # Placeholder where the selected graph will be displayed
            html.Div(id='insulin-graph-container')
        ])
     ])

    elif tab == 'tab-aglp1':
        # Generate the interactive Plotly line graph
        line_fig = create_plotly_line_graph()
        # Generate the value boxes
        value_boxes = create_value_boxes()
        return html.Div([
    html.H3('Understanding aGLP-1 Administration Challenges and Medication Errors'),
    html.Div([
        html.Div(dcc.Graph(figure=line_fig), style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
        html.Div(value_boxes, style={'width': '50%', 'display': 'inline-block', 'padding': '20px'}),
    ], style={'display': 'flex', 'justifyContent': 'space-between'}),
# Adding the dropdown selection bar for graph options
    html.Div([
        html.H5("Please select a graphic option that you want to visualize : ", style={'textAlign': 'left', 'marginBottom': '10px', 'fontSize' : '15px'}),
        dcc.Dropdown(
            id='aglp1-graph-dropdown',
            options=[
                {'label': 'Distribution of Medication Errors', 'value': 'histogram'},
                {'label': 'Incidents per Type of Case', 'value': 'bar'},
                {'label': 'Type of Declaration per Year', 'value': 'declaration'}
        ],
        value='histogram', 
        clearable=False,
        style={'width': '50%', 'marginLeft': '30px', 'paddingBottom': '10px'}
    ),

    # Placeholder where the selected graph will be displayed
    html.Div(id='aglp1-graph-container')  # Ensure correct alignment here
        ])
    ])
    
    elif tab == 'tab-about':
        return html.Div([
            html.Img(
                src='https://www.iqviamedicalsalescareers.com/img/d49b1e82-4816-4370-536b-08da8113e407', 
                style={'width': '100%', 'height': '400px', 'objectFit': 'cover', 'marginBottom': '50px'}  # Increase marginBottom to 30px
            ),  
            html.H2(
                'About our project',
                style={
                    'color': 'black', 
                    'fontSize': '30px',  # Text size
                    'textAlign': 'center',  # Center align text
                    'margin': '0',  # No margin around the text
                }
            ),
            html.H4(
    'The research was conducted '
    'by Doğa Can as part of the Master\'s degree in Health Engineering with a specialization in Data Science for '
    'Health at the University of Lille\'s Faculty of Health Management and Engineering (ILIS). The project '
    'was completed during the 2023-2024 academic year, and the final thesis defense took place on June 26, 2024.',
    style={
        'color': 'black',
        'fontSize': '25px',  # Text size
        'textAlign': 'justify',  # Justify text alignment for a professional look
        'marginTop': '20px',  # Add margin to the top of the paragraph
        'maxWidth': '1500px',  # Limit width to make text more readable
        'marginLeft': 'auto',  # Center the block horizontally
        'marginRight': 'auto',  # Center the block horizontally
        'fontWeight': 'normal'  # Set the font weight to normal (not bold)
    }
),

            html.H4('This work was supervised by Dr. Michaël Rochoy, whose guidance and support were essential in shaping the research. The project also received valuable feedback from a jury led by Prof. Dr. Benjamin Guinhouya. Other members of the jury, including Dr. Djamel Zitouni, Dr. François Dufossez, and Fabio Boudis, provided insightful contributions throughout the process.',
                style={
                    'color': 'black', 
                    'fontSize': '25px',  # Text size
                    'textAlign': 'justify',  # Justify text alignment for a professional look
                    'marginTop': '20px',  # Add margin to the top of the paragraph
                    'maxWidth': '1500px',  # Limit width to make text more readable
                    'marginLeft': 'auto',  # Center the block horizontally
                    'marginRight': 'auto',  # Center the block horizontally
                    'fontWeight': 'normal'  # Set the font weight to normal (not bold)
                }
            ),
            html.H4('The University of Lille and the ILIS Faculty played a crucial role in supporting this research, offering both academic resources and a stimulating environment. The French National Pharmacovigilance Database, which provided data on adverse reactions reported between 1988 and 2022, was a key resource in identifying patterns and trends related to medication errors involving insulin and aGLP-1 autoinjectors. A special thank you goes to Pr. Sophie Gautier for her help in accessing this vital data.',
                style={
                    'color': 'black', 
                    'fontSize': '25px',  # Text size
                    'textAlign': 'justify',  # Justify text alignment for a professional look
                    'marginTop': '20px',  # Add margin to the top of the paragraph
                    'maxWidth': '1500px',  # Limit width to make text more readable
                    'marginLeft': 'auto',  # Center the block horizontally
                    'marginRight': 'auto',  # Center the block horizontally
                    'fontWeight': 'normal'  # Set the font weight to normal (not bold)
                }
            )
        ], style={
            'textAlign': 'center',  # Center align the contents of the Div
            'display': 'flex',
            'flexDirection': 'column',
            'alignItems': 'center',  # Center align items horizontally
            'justifyContent': 'center',  # Center align items vertically
        })

@app.callback(
    Output('insulin-graph-container', 'children'),
    Input('insulin-graph-dropdown', 'value')
)
def update_insulin_graph(selected_graph):
    if selected_graph == 'histogram':
        # Option 1: Show Distribution of Medication Errors (Histogram)
        fig = create_plotly_insulin_histogram()
        fig.update_layout(height=700, width=900)  # Increase size of the histogram
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # Center this graph
    elif selected_graph == 'bar':
        # Option 2: Show Incidents per Type of Case (Bar)
        fig = create_plotly_insulin_bar_by_sex()
        fig.update_layout(height=700, width=900)  # You can adjust the size here if needed
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # No centering applied here
    elif selected_graph == 'declaration':
        # Option 3: Show Type of Declaration per Year
        fig = create_plotly_insulin_declaration_graph()
        fig.update_layout(height=700, width=900)  # Increase size of the declaration graph
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # Center this graph

@app.callback(
    Output('aglp1-graph-container', 'children'),
    Input('aglp1-graph-dropdown', 'value')
)
def update_aglp1_graph(selected_graph):
    if selected_graph == 'histogram':
        # Option 1: Show Distribution of Medication Errors (Histogram)
        fig = create_plotly_histogram()
        fig.update_layout(height=700, width=900)  # Increase size of the histogram
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # Center this graph
    elif selected_graph == 'bar':
        # Option 2: Show Incidents per Type of Case (Bar)
        fig = create_plotly_bar_plot()
        fig.update_layout(height=700, width=900)  # You can adjust the size here if needed
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # No centering applied here
    elif selected_graph == 'declaration':
        # Option 3: Show Type of Declaration per Year
        fig = create_plotly_declaration_graph()
        fig.update_layout(height=700, width=900)  # Increase size of the declaration graph
        return html.Div(dcc.Graph(figure=fig), style={'width': '70%', 'margin': '0 auto'})  # Center this graph

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8050))  # Use Render's port if available, otherwise default to 8050
    app.run_server(host='0.0.0.0', port=port, debug=True)

