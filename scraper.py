import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date

batters_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim"
pitchers_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim"


###############################################################################
# package GET request, send & catch response. Retrieve form data for a POST request
###############################################################################

r = requests.get(batters_url)
html_doc = r.text
tag_soup = BeautifulSoup(html_doc, 'html.parser')

###############################################################################
# Capture Form Data Parameters programmatically by parsing HTML form tags
###############################################################################

form_info = tag_soup.find_all('input',{"id" : {"__VIEWSTATE", "__EVENTVALIDATION"}})

# initialize dict to store all params.
param_dict = {"__EVENTTARGET" : "DFSBoard1$cmdCSV"}

# parse form_info, update dict.
for i in range(len(form_info)):
    key = form_info[i]['id']
    param_dict[key] = form_info[i]['value']

# set the encoding headers of the HTTP request
headers = {'Content-Type' : 'application/x-www-form-urlencoded'}

###############################################################################
# Make POST request to retrieve CSV data using the parsed form data above,
###############################################################################

# package the POST request, send & catch response
r = requests.post(batters_url, data=param_dict, headers=headers)
print(r.status_code, r.ok)

# extract response data
sim_text = r.text

###############################################################################
# Parse text into rows
###############################################################################

sim_text = list(sim_text.strip().replace('"', '').split('\r\n'))

# remove double quotes, split row each row into a sublist per player
sim_list = [player.split(',') for player in sim_text]
col_names = sim_list.pop(0)
col_names[0] = 'Name'
# convert nested list of lists into list of tuples
sim_list_tup = [tuple(l) for l in sim_list]

sim_df = pd.DataFrame.from_records(sim_list_tup,
                                   columns=col_names,
                                   coerce_float=True)

# Columns that can be converted to a numeric type will be converted
sim_df = sim_df.apply(pd.to_numeric, errors='ignore')


###############################################################################
# Add a Date Column
###############################################################################

# Create a Date column for today's date.
today = date.today().isoformat()
today_array = pd.Series([today] * sim_df.shape[0])

# to_datetime parses a date representation into a date type format.
sim_df['Date'] = pd.to_datetime(today_array, format="%Y-%m-%d")

# check data
sim_df.dtypes
sim_df.shape

###############################################################################
# Append Dataframe to existing File on disk.
###############################################################################

# Need to run the lines above twice, once using batter_url, and then another
# time substituting the pitcher_url. During each process use the context
# manager below with the relevant data frame (line 96).

batters_path = '/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_batters.csv'
pitchers_path = '/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_pitchers.csv'


# open context manager to append batters dataframes to existing file, auto close.
with open(batters_path, 'a') as f:
    sim_df.to_csv(f, index=False, header=False)



# check the updated df for batters
batters_total_df = pd.read_csv('/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_batters.csv')

# check the updated df for pitchers
pitchers_total_df = pd.read_csv('/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_pitchers.csv')
