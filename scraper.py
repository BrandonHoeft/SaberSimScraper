# run module to scrape and append today's new hitter, pitcher projections.

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import os



def get_form_data(url):
    """Through a GET request, return a dictionary of key:value form data
    relating to the 'Export Data' button on webpage. The form data is needed
    for POST request to the web server to retrieve the player projection data.
    Useful in the event that Fangraphs changes the form data values.
    """

    html_doc = requests.get(url).text
    soup = BeautifulSoup(html_doc, 'html.parser')
    form_info = soup.find_all('input', 
                              {"id" : {"__VIEWSTATE", "__EVENTVALIDATION"}})

    # initialize dict to store all params.
    param_dict = {"__EVENTTARGET" : "DFSBoard1$cmdCSV"}
    # parse form_info, update dict.
    for i in range(len(form_info)):
        key = form_info[i]['id']
        param_dict[key] = form_info[i]['value']

    return param_dict




def scrape_data(url, form_data):
    """Makes a POST request to the Fangraphs web server and retrieves the
    player projection data as a single large text string. The default returned
    text is double-quoted, comma-separated values.
    """

    # set encoding headers of the HTTP request
    headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
    # package the POST request, send & catch response
    r = requests.post(url, data=form_data, headers=headers)
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
    col_names = data_list.pop(0)
    col_names[0] = 'Name'

    # convert list of lists into list of tuples
    data_list = [tuple(l) for l in data_list]
    # list to DataFrame
    df = pd.DataFrame.from_records(data_list,
                                   columns=col_names,
                                   coerce_float=True)
    # coerce to numeric columns if possible.
    df = df.apply(pd.to_numeric, errors='ignore')
    
    return df




def series_today_date(df):
    """create a pandas Series of the same length as an existing data frame
    that captures today's date as a datetime64 type.
    """

    today = date.today().isoformat()
    today_array = pd.Series([today] * df.shape[0])
    return pd.to_datetime(today_array, format="%Y-%m-%d")


def write_to_csv(df, file_path, mode='a'):
    """write a dataframe to a .CSV file path on disk. Anticipates 2 modes: 'w'
    for writing to new file, or 'a' for appending to an existing file path. 
    >>> write_date(batter_df, '/Users/myname/Desktop/projections.csv', 'a')
    "success: added 252 rows to file."
    """        
    if mode == 'a':
        # check that for append mode, a file exists to append. if not, exit.
        if not os.path.exists(file_path):
            print('error:', file_path, 'does not exist.')
            return # return none, exits func.

        with open(file_path, 'a') as f:
            df.to_csv(f, index=False, header=False)
        print('success: added {0} rows to {1}'.format(df.shape[0], file_path))

    elif mode == 'w':
        with open(file_path, 'w') as f:
            df.to_csv(f, index=False, header=True)
        print('success: new file with {} rows and {} columns'.format(*df.shape))

    else:
        print('something did not work as expected. investigate...')




if __name__ == '__main__':
    
    # ID hitter/pitcher urlsfor scraping, local file paths for writing. 
    hitters_url = 'https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim'  
    hitters_out = '/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_batters.csv'
    pitchers_url = 'https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim'
    pitchers_out = '/Users/bhoeft/Desktop/baseball_data_dfs/SaberSim/sabersim_pitchers.csv'
    locations = [[hitters_url, hitters_out],
                 [pitchers_url, pitchers_out]]
    
    # loop over hitter, pitcher url/file path and apply 
    # same scrape, parse, transform, write process.
    for i in range(len(locations)):
        param_dict = get_form_data(locations[i][0])
        text = scrape_data(locations[i][0], form_data=param_dict)
        df = parse_text_to_df(text)
        df['Date'] = series_today_date(df)
        write_to_csv(df, locations[i][1], 'a')