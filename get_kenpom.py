from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

years = ['2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019', '2020']

url = "https://kenpom.com/index.php?y="
team_info = []

print("Staring scraping for kenpom...")
for year in years:
    print('starting {}'.format(year))
    soup = BeautifulSoup(urlopen(url+ year).read(), 'html.parser')
    table = soup.find_all('tbody')[0]
    for row in table.find_all('tr'):
        tds = row.find_all('td')
        if(len(tds) > 0):
            team_info.append([year, tds[1].find('a').get_text(),tds[4].get_text(), tds[5].get_text(), tds[7].get_text(), tds[13].get_text()])
            
team_info = pd.DataFrame(team_info, columns = ['Season', 'TeamName','kp_rating', 'off_eff', 'def_eff', 'kp_sos'])
team_info.to_pickle("kenpom_df")


print("finished scraping kenpom data")