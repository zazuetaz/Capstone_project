import pandas as pd
import plotly.graph_objs as go
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import joblib
from joblib import load
from assorted_dicts import nbhood_stations
from assorted_dicts import nbhood_station
from assorted_dicts import stat_counts


#App basics
BASE_URL = "http://localhost:5000"

#This is the selected formating for the SS
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#Instantiating the app and specifying formating
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)

server = app.server


#Inputs
#This sets up an input numeric text box for weather
input_weather = dcc.Input(id='weather-input',
                          placeholder='Temp in degrees F',
                          type='number',
                          value='55')

#This sets up a list of available neighborhood options for the user to select
nbhood = ['Astoria', 'Battery Park', 'Bedford Stuyvesant', 'Boerum Hill', 'Brooklyn Heights', 'Bushwick',
          'Carnegie Hill', 'Carroll Gardens', 'Central Park', 'Chelsea', 'Chinatown', 'Clinton',
          'Clinton Hill', 'Cobble Hill', 'Columbia Street Waterfront District', 'Columbus Circle',
          'Crown Heights', 'DUMBO', 'Downtown', 'East Harlem', 'East Village', 'Financial District',
          'Flatiron District', 'Fort Greene', 'Garment District', 'Gowanus', 'Gramercy', 'Greenpoint',
          'Greenwich Village', 'Greenwood', 'Harlem', 'Hunters Point', 'Journal Square',
          'Little Italy', 'Lower East Side', 'Manhattanville', 'Midtown', 'Morningside Heights',
          'Murray Hill', 'Navy Yard', 'NoHo', 'Park Slope', 'Prospect Heights',
          'Prospect Lefferts Gardens', 'Red Hook', 'SoHo', 'Stuyvesant Town', 'Sunnyside',
          'Sunset Park', 'Sutton Place', 'The Waterfront', 'Tribeca', 'Tudor City', 'Turtle Bay',
          'Upper East Side', 'Upper West Side', 'West Village', 'Williamsburg']

nbn = {'Battery Park': 1, 'Bedford Stuyvesant': 2, 'Boerum Hill': 3, 'Brooklyn Heights': 4, 'Bushwick': 5,
       'Carnegie Hill': 6, 'Carroll Gardens': 7, 'Central Park': 8, 'Chelsea': 9, 'Chinatown': 10, 'Clinton': 11,
       'Clinton Hill': 12, 'Cobble Hill': 13, 'Columbia Street Waterfront District': 14, 'Columbus Circle': 15,
       'Crown Heights': 16, 'DUMBO': 17, 'Downtown': 18, 'East Harlem': 19, 'East Village': 20, 'Financial District': 21,
       'Flatiron District': 22, 'Fort Greene': 23, 'Garment District': 24, 'Gowanus': 25, 'Gramercy': 26, 'Greenpoint': 27,
       'Greenwich Village': 28, 'Greenwood': 29, 'Harlem': 30, 'Hunters Point': 31, 'Journal Square': 32,
       'Little Italy': 33, 'Lower East Side': 34, 'Manhattanville': 35, 'Midtown': 36, 'Morningside Heights': 37,
       'Murray Hill': 38, 'Navy Yard': 39, 'NoHo': 40, 'Park Slope': 41, 'Prospect Heights': 42,
       'Prospect Lefferts Gardens': 43, 'Red Hook': 44, 'SoHo': 45, 'Stuyvesant Town': 46, 'Sunnyside': 47,
       'Sunset Park': 48, 'Sutton Place': 49, 'The Waterfront': 50, 'Tribeca': 51, 'Tudor City': 52, 'Turtle Bay': 53,
       'Upper East Side': 54, 'Upper West Side': 55, 'West Village': 56, 'Williamsburg': 57}

#This creates a dropdown for the neighborhoods
nbhoods = [{'label': nb, 'value': nb} for nb in nbhood]
dropdown_nbh = dcc.Dropdown(
    id = 'nbhood-dropdown',
    options = nbhoods,
    value = 'Astoria',
    style={'width': '50%'}
)

#This calls in the dictionary of neighborhoods and their stations
stat_names = list(nbhood_station.keys())
nestedOptions_statnames = nbhood_station[stat_names[0]]
stnames = [{'label':stat_name, 'value': stat_name} for stat_name in stat_names]
dropdown_statname = dcc.Dropdown(
    id = 'statname-dropdown',
    options = stnames,
    value = 'Astoria',
    style={'width': '50%'}
)

namedstations = dcc.Dropdown(
    id = 'namedstation-dropdown',
    style={'width': '50%'}
)

#This creates a dropdown for the days of the week
DOW = {'Monday': 'dow_0', 'Tuesday': 'dow_1', 'Wednesday': 'dow_2', 'Thursday': 'dow_3', 'Friday': 'dow_4',
       'Saturday': 'dow_5', 'Sunday': 'dow_6'}

down = {'dow_1': 59, 'dow_2': 60, 'dow_3': 61,
        'dow_4': 62, 'dow_5': 63, 'dow_6': 64}

day_of_week_for_counts = {'dow_0': '0', 'dow_1': '1', 'dow_2': '2', 'dow_3': '3', 'dow_4': '4', 'dow_5': '5', 'dow_6': '6'}

wkndn = {'weekend?_1': 64}

dayofweek = [{'label': key, 'value': DOW[key]} for key in DOW.keys()]
dropdown_dow = dcc.Dropdown(
    id = 'dow-dropdown',
    options = dayofweek,
    value = 'Monday',
    style={'width': '50%'}
)

#This creates a dropdown for the hours of the day
Hour = {'12am': 'hour_0', '1am': 'hour_1', '2am': 'hour_2', '3am': 'hour_3', '4am': 'hour_4', '5am': 'hour_5',
        '6am': 'hour_6', '7am': 'hour_7', '8am': 'hour_8', '9am': 'hour_9', '10am': 'hour_10', '11am': 'hour_11',
        '12pm': 'hour_12', '1pm': 'hour_13', '2pm': 'hour_14', '3pm': 'hour_15', '4pm': 'hour_16', '5pm': 'hour_17',
        '6pm': 'hour_18', '7pm': 'hour_19', '8pm': 'hour_20', '9pm': 'hour_21', '10pm': 'hour_22', '11pm': 'hour_23'}

hodn = {'hour_1': 65, 'hour_2': 66, 'hour_3': 67, 'hour_4': 68, 'hour_5': 69, 'hour_6': 70, 'hour_7': 71, 'hour_8': 72,
        'hour_9': 73, 'hour_10': 74, 'hour_11': 75, 'hour_12': 76, 'hour_13': 77, 'hour_14': 78, 'hour_15': 79,
        'hour_16': 80, 'hour_17': 81, 'hour_18': 82, 'hour_19': 83, 'hour_20': 84, 'hour_21': 85, 'hour_22': 86,
        'hour_23': 87}

hour_for_count = {'hour_0': '0', 'hour_1': '1', 'hour_2': '2', 'hour_3': '3', 'hour_4': '4', 'hour_5': '5', 'hour_6': '6',
                  'hour_7': '7', 'hour_8': '8', 'hour_9': '9', 'hour_10': '10', 'hour_11': '11', 'hour_12': '12',
                  'hour_13': '13', 'hour_14': '14', 'hour_15': '15', 'hour_16': '16', 'hour_17': '17', 'hour_18': '18',
                  'hour_19': '19', 'hour_20': '20', 'hour_21': '21', 'hour_22': '22', 'hour_23': '23'}


hourofday = [{'label': key, 'value': Hour[key]} for key in Hour.keys()]
dropdown_hod = dcc.Dropdown(
    id = 'hod-dropdown',
    options = hourofday,
    value = '12am',
    style={'width': '50%'}
)


input_statcount = dcc.Input(id='count_key')

cols = ['tempF', 'neighborhood_Battery Park', 'neighborhood_Bedford Stuyvesant', 'neighborhood_Boerum Hill',
        'neighborhood_Brooklyn Heights', 'neighborhood_Bushwick', 'neighborhood_Carnegie Hill', 'neighborhood_Carroll Gardens',
        'neighborhood_Central Park', 'neighborhood_Chelsea', 'neighborhood_Chinatown', 'neighborhood_Clinton',
        'neighborhood_Clinton Hill', 'neighborhood_Cobble Hill', 'neighborhood_Columbia Street Waterfront District',
        'neighborhood_Columbus Circle', 'neighborhood_Crown Heights', 'neighborhood_DUMBO', 'neighborhood_Downtown',
        'neighborhood_East Harlem', 'neighborhood_East Village', 'neighborhood_Financial District',
        'neighborhood_Flatiron District', 'neighborhood_Fort Greene', 'neighborhood_Garment District', 'neighborhood_Gowanus',
        'neighborhood_Gramercy', 'neighborhood_Greenpoint', 'neighborhood_Greenwich Village', 'neighborhood_Greenwood',
        'neighborhood_Harlem', 'neighborhood_Hunters Point', 'neighborhood_Journal Square', 'neighborhood_Little Italy',
        'neighborhood_Lower East Side', 'neighborhood_Manhattanville', 'neighborhood_Midtown', 'neighborhood_Morningside Heights',
        'neighborhood_Murray Hill', 'neighborhood_Navy Yard', 'neighborhood_NoHo', 'neighborhood_Park Slope',
        'neighborhood_Prospect Heights', 'neighborhood_Prospect Lefferts Gardens', 'neighborhood_Red Hook', 'neighborhood_SoHo',
        'neighborhood_Stuyvesant Town', 'neighborhood_Sunnyside', 'neighborhood_Sunset Park', 'neighborhood_Sutton Place',
        'neighborhood_The Waterfront', 'neighborhood_Tribeca', 'neighborhood_Tudor City', 'neighborhood_Turtle Bay',
        'neighborhood_Upper East Side', 'neighborhood_Upper West Side', 'neighborhood_West Village', 'neighborhood_Williamsburg',
        'dow_1', 'dow_2', 'dow_3', 'dow_4', 'dow_5', 'dow_6', 'weekend?_1', 'hour_1', 'hour_2', 'hour_3', 'hour_4',
        'hour_5', 'hour_6', 'hour_7', 'hour_8', 'hour_9', 'hour_10', 'hour_11', 'hour_12', 'hour_13', 'hour_14',
        'hour_15', 'hour_16', 'hour_17', 'hour_18', 'hour_19', 'hour_20', 'hour_21', 'hour_22', 'hour_23', 'stat_size_Large',
        'stat_size_Medium', 'stat_size_Small', 'ct_revised']

#Here is the app layout
app.layout = html.Div([
    #This is the page title
    html.H1("Citibike Trip Planner"),
    #Instruction for the user
    html.H4('Input the predicted temp'),
    #Calling the input box from above
    input_weather,
    #Bringing in a callback - see below code
    html.Div(id='weather-temp'),
    #Instructions
    html.H4('Select a neighborhood'),
    #Station name dropdown
    dropdown_statname,
    #Instructions
    html.H4('Select a station'),
    #Dynamic station name dropdown
    namedstations,
    #Instruction
    html.H4('Select the day of the week'),
    #dropdown for day of week
    dropdown_dow,
    #Callback for dow
    html.H4('Select the hour of the day'),
    dropdown_hod,
    html.H4('The predicted availability of bikes in the selected station at the chosen time is:'),
    html.Div(id='result')
])

@app.callback(Output('namedstation-dropdown', 'options'),
              [Input('statname-dropdown', 'value')])

def update_statname_dropdown(name):
    return [{'label': i, 'value':i} for i in nbhood_station[name]]


@app.callback(Output('result', 'children'),
              [Input('weather-input', 'value'),
               Input('statname-dropdown', 'value'),
               Input('dow-dropdown', 'value'),
               Input('hod-dropdown', 'value'),
               Input('namedstation-dropdown', 'value')])

def predict_avail(nums, nbhs, dows, hods, station):
    s = '0'
    t = '0'
    g = [0] * 92
    # Sets the first value to b, the temp
    if not nums:
        nums == 54
    g[0] = nums
    if not nbhs:
        nbhs == 'Astoria'
    if not dows:
        dows == 0
    if not hods:
        hods == '12am'
    # Sets the neighborhood
    if nbhs != 'Astoria':
        i = nbn[nbhs]
        g[i] = 1
    # Sets the day of the week - keeps everything as 0 if dow is Monday(0)
    if dows != 'Monday':
        j = down[dows]
        g[j] = 1
        s = day_of_week_for_counts[dows]
        # Sets the weekend? field to 1 if dow is 5 or 6
        if j == 62 or j == 63:
            k = wkndn['weekend?_1']
            g[k] = 1
    # Sets the hour of the day
    if hods != '12am':
        m = hodn[hods]
        g[m] = 1
        t = hour_for_count[hods]
    key = s + ' - ' + t
    if not station:
        station = 'Queens Plaza North & Crescent St'
    ct = stat_counts[station][key]
    g[91] = ct
    y = nbhood_stations[nbhs][station]
    if y != 'Extra Large':
        z = 88 if y == 'Large' else 89 if y == 'Medium' else 90
        g[z] = 1
    g = pd.DataFrame([g], columns=cols)
    x = model.predict(g)[0]
    return x

if __name__ == '__main__':
    model = joblib.load('rf_mod_1.joblib')
    app.run_server(debug=True)

