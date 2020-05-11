from urllib.request import urlopen
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import matplotlib.pyplot as plt

years = ['2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','2017','2018','2019', '2020']
#Change to https://www.teamrankings.com/ncaa-basketball/rpi-ranking/rpi-rating-by-team?date=2018-03-01 when you have a chance
# Paper citing changes aren't significant in the end of the year, while changes after the tourny will be bad for explaining 
# new games
url = "https://www.teamrankings.com/ncaa-basketball/rpi-ranking/rpi-rating-by-team?date="  
day = "-03-02"
r = []
team_rpi = []

print("Staring scraping for RPI...")
for year in years:
    print('starting {}'.format(year))
    soup = BeautifulSoup(urlopen(url+ year + day).read(), 'html.parser')
    table = soup.find_all('tbody')[0]
    for row in table.find_all('tr'):
        tds = row.find_all('td')
        if(len(tds) > 0):
            name_array = tds[1].get_text().split('(')[:-1]
            if(len(name_array) > 1):
                name = name_array[0] + '(' + name_array[1][:-1]
            else:
                name = name_array[0][:-1]
            team_rpi.append([year, name, tds[2].get_text()])
        else:
            break
            
team_rpi = pd.DataFrame(team_rpi, columns = ['Season', 'TeamName', 'rpi'])
team_rpi.to_pickle("rpi")


print("finished writing rpi to csv.")