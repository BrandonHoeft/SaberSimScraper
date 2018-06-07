import requests
from bs4 import BeautifulSoup

team_id = 1
team_batters_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=bat&type=sabersim&team=" + str(team_id)
all_pitcher_url = "https://www.fangraphs.com/dailyprojections.aspx?pos=all&stats=pit&type=sabersim"

# package the GET request, send & catch response
r = requests.get(team_batters_url)

# extract response HTML structure
html_doc = r.text

# parse, prettify, extract data from HTML
tag_soup = BeautifulSoup(html_doc, 'html.parser')

# return HTML parse tree in nice formatted string,  each HTML/XML tag per own line
pretty_soup = tag_soup.prettify()

# extract text from HTML tree
tag_soup.get_text()

# PLACEHOLDER: Note that I may need to incorporate pagination, complex parsing.
# https://bit.ly/2LiUSTN
# https://github.com/bwainstock/baseball-scraper




