# NOTE TO SELF: spin this up as a jupyter notebook first before doing further
# Development. Will be a good future learning resource. 

import requests
from bs4 import BeautifulSoup
import pandas as pd 

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

# Used Chrome Dev tools to identify the form params needed potentially, and the
# postman app to test which subset will yield a successful POST of the .csv data.
# just needed 3: EVENTTARGET, VIEWSTATE, EVENTVALIDATION.
form_info = tag_soup.find_all('input',{"id" : {"__VIEWSTATE", "__EVENTVALIDATION"}})

# initialize dict to store all params.
param_dict = {"__EVENTTARGET" : "DFSBoard1$cmdCSV"}

# update dict after parsing form info above.
for i in range(len(form_info)):
    key = form_info[i]['id']
    param_dict[key] = form_info[i]['value']


# set the type of the body for the HTTP request as headers. Per wikipedia
# https://en.wikipedia.org/wiki/Percent-encoding#The_application/x-www-form-urlencoded_type
# When sent in an HTTP POST request or via email, the data is placed in the 
# body of the message, and application/x-www-form-urlencoded is included in the 
# message's Content-Type header
headers = {'Content-Type' : 'application/x-www-form-urlencoded'}


###############################################################################
# Make POST request to retrieve CSV data using the parsed form data above,
# https://en.wikipedia.org/wiki/POST_(HTTP)
# tested using Postman to make sure have right parameters
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

# Create a Date column for today's date. 


