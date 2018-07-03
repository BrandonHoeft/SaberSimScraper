import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date


batters_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim"
pitchers_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim"


def get_form_data(url):
    """Through a GET request, return a dictionary of key:value form data
    relating to the 'Export Data' button on webpage. The form data is needed
    for POST request to the web server to retrieve the player projection data.
    Useful in the event that Fangraphs changes the form data values.
    """

    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    info = tag_soup.find_all('input',{"id" : {"__VIEWSTATE", "__EVENTVALIDATION"}})

    # initialize dict to store all params.
    param_dict = {"__EVENTTARGET" : "DFSBoard1$cmdCSV"}
    # parse form_info, update dict.
    for i in range(len(info)):
        key = form_info[i]['id']
        param_dict[key] = form_info[i]['value']

    return param_dict




def scrape_data(url):
    """Makes a POST request to the Fangraphs web server and retrieves the
    player projection data as a single large text string. The default returned
    text is double-quoted, comma-separated values.
    """

    # set encoding headers of the HTTP request
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    # package the POST request, send & catch response
    r = requests.post(url, data=param_dict, headers=headers)
    print(r.status_code, r.ok)

    return r.text




def parse_text_to_df(txt):
    """parses the scraped text string into a pandas dataframe for analysis.
    """
    # returns a list of n player strings by parsing on newline
    data_list = list(txt.strip().replace('"', '').split('\r\n'))
    # remove double quotes, split each player string into a sublist
    data_list = [player.split(',') for player in data_list]

    # first row are col headers.
    col_names = sim_list.pop(0)
    col_names[0] = 'Name'

    # convert list of lists into list of tuples
    data_list = [tuple(l) for l in data_list]
    # list to DataFrame
    df = pd.DataFrame.from_records(sim_list_tup,
                                   columns=col_names,
                                   coerce_float=True)
    # coerce to numeric columns if possible.
    df = sim_df.apply(pd.to_numeric, errors='ignore')


# TO DO LIST
# 1. Function for Adding a Date column to the DataFrame
# 2. Function to open a context manager for appending dataframe to existing
#   CSV or writing to a new CSV
# 3. Need to write code to execute the file if the module name == __main__
#   http://ibiblio.org/g2swap/byteofpython/read/module-name.html
#   https://stackoverflow.com/questions/419163/what-does-if-name-main-do
# 4. NEED TO TEST FUNCTIONS. Create a unit_tests.py.
