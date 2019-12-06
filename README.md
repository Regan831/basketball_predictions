# basketball_predictions for NCAA games. 

Data taken from Kaggle (https://www.kaggle.com/ncaa/ncaa-basketball).
This is a work in progress and will be updately continually. Currently in progress, an exploration of teams that are similar to each other to determine the number of wins a team will have in the NCAA tournament. This uses a method similar to a recommender system.

data_load.ipynd is used to load data from csv files and does necessary pre-processing. This file reads, creates new stats, merges into a select number of pandas dataframes then exported to a pickle file. This notebook also provides a slight introduction to the NCAA tournament. (Still has more than just initial data load)

EDA.ipynb explores the data of past games back to 1985. Findings in this are included to performance by seeds, underdogs and upsets, champtionships, conferences, and stats that can be used to explain a good team. Additional comments are in the file to go along with the graphs to explain what the graphs mean and to provide analysis of the graphics.

get_rpi.py is a scraper that scrapes from a website to get all RPI rankings from 2003 to 2019. Improvements can be made to change the date to pull, number of years to select and other performance metrics such as kenpom. Currently pulls from March 2nd, a safe date to pull from that is before the tourney every year.
