# Capstone_project
Final capstone project

Introduction and Business Problem
New York City residents utilize a number of modes of transportation to get from place to place and need to know they can rely on their preferred mode when they need it. One popular method is the shared bike system operated by Citibike. Citibike has stations in Manhattan, Queens, Brooklyn, and Jersey City. While Citibike does offer information in their application about the real-time availability of their bikes at a given station, there is no application that would allow a biker to know ahead of time whether they can rely on a bike being available at their station of choice (that I know of).

I will aim to solve that problem by constructing a dash application a Citibike user could utilize to plan a trip using a bike from their station of choice.

Data
The data for this project will come from Citibike System Data. Ideally I would be able to run an API call on their station information, collecting minute by minute availability of bike traffic over the course of the day for a number of weeks. However, at the time I was collecting information for this project, NYC was under a shelter-in-place order to help stop the spread of the novel coronavirus, COVID-19. Given the halt on normal city traffic, I needed a different approach.

I had to utilize rider data from April 2019 and manipulated it to generate a rolling count of bikes being checked in and out of stations. I paired that traffic data with other general information about the stations and ended up with a dataset that had approximate station counts for 741 stations 24/7 for the month. I made daily adjustments to the counts to account for station capacity, and believe this adjustment roughly captured the process of station refilling - where Citibike will shift bikes en masse during off hours to restock empty stations that are popular start points but unpopular destination stations/remove bikes from popular destination stations so more bikes can be docked there.

I also wanted to use weather as a predictive input - intuitively there will likely be more bike traffic when it is nice out and less bike traffic when there is inclement weather.

And while some geographical information was provided in the Citibike datasets, I knew I wanted to pull in more granular information, specifically the NYC neighborhoods where the stations were located.

Data Sourcing
The citibike information comes from two places.

The station information is pulled from their APIs: http://gbfs.citibikenyc.com/gbfs/gbfs.json.
The historical data I use is coming from their Citi Bike Daily Ridership and Membership Data here: https://www.citibikenyc.com/system-data
I use historical weather data from New York that is sourced from the World Weather Online Developer Portal API here: https://www.worldweatheronline.com/developer/api/docs/historical-weather-api.aspx

I use MapBox for geospatial data to identify NYC neighborhoods

Process
After gathering and cleaning the data, I fit and tuned various Machine Learning classification models to predict, given a number of inputs, a classification problem of whether the number of bikes at the station at a given time will be low, medium, or high.

The output is code for a web based application deployed in dash.
