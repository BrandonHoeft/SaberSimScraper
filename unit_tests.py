# testing the functions in scraper.py
import os
from datetime import date

os.path.expanduser('~') # root home dir
os.getcwd() # current
desired_path = 'Desktop/SaberSimScraper'
os.chdir(desired_path)


import scraper

# Test 1: test get_form_data(). Should return dict of 3 key:val pairs
###############################################################################

url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim"
test1 = scraper.get_form_data(url)

if len(test1.values()) == 3 and type(test1) == dict:
    test1_result = True


# Test 2: test scrape_data(url, form_data). Should return a non-zero length string.
###############################################################################


test2 = scraper.scrape_data(url, form_data=test1) # use test1 as 2nd arg input

if len(test2) > 0 and type(test2) == str:
    test2_result = True
    
# Test 3: test parse_text_to_df(txt). Should yield dataframe with >50 rows, 20 cols
###############################################################################

test3 = scraper.parse_text_to_df(test2)
rows, cols = test3.shape

if rows > 50 and cols == 20: 
    test3_result = True


# Test 4: test series_today_date(df). Should return pandas Series of same 
# length as test3 rows count, containing today's date.
###############################################################################

test4 = scraper.series_today_date(test3)
test4_unique_date = str(test4.unique()[0])[0:10]

if len(test4) == rows and test4_unique_date == date.today().isoformat():
    test4_result = True


# Test 5: test  write_to_csv(df, file_path, mode='a'). Should append to existing
#   file or write/overwrite a filepath specified depending on the mode.
###############################################################################

test5_path = 'sabersim_batters_TEST.csv'

# test5_path does not exist in github directory. Should fail and print error.
scraper.write_to_csv(test3, test5_path, 'a')
# write to new file. Should get a success log statement. 
scraper.write_to_csv(test3, test5_path, 'w')
# append data to newly written file. Should get a success log statement. 
scraper.write_to_csv(test3, test5_path, 'a')

test5_result = os.path.exists(test5_path)


# Did any of test 1-5 fail?
###############################################################################

if (test1_result and test2_result and test3_result and test4_result and test5_result):
    print('All Tests passed!')
else:
    print('Some Tests failed.')