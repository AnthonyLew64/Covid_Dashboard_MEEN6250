# Covid_Dashboard_MEEN6250

Yousef Alsanea

Anthony Lew

ME EN 6250

University of Utah

Course Project

11 Dec 2022


Covid Dashboard Project for ME EN 6250 course

This project will scrape data from a Covid death tracking website to be used in a graphical dashboard interface

The module ScrapeWebsite.py has been added. 
This module uses the json, requests, bs4, datetime, and os python libraries.
This module will pull country names and total and new data for cases and deaths (in absolute and per 1 million) from the https://www.worldometers.info/coronavirus/#countries website.
The module will pull global cumulative case and death data as well as 7 day rolling average data for new cases and new deaths from the https://covid19.who.int/table wbsite.
A dictionary is created from this data with nested keys starting with day (yyyy-mm-dd string format), country name (or "World") and then data type ("Total Cases" or "New Deaths /1M"). 
Each new day is appended to the dictionary in the json file (or a new file is created if a json does not already exist).
Each day's dictionary is also saved as it's own json file for backup, named "<date>.json" (2022-11-21.json).
This module includes functions:
scrape_website -- to pull data from a website and save the days data to a backup file and append the data to the Scraped_Data.json file
scrape_country -- to pull a single country's data from a website for today
append_date -- to arbitrarily add a day's data to the Scraped_Data.json given the data has already been stored as a dated backup file
  
Dated .json files contain dictionaries with the data from previous days that have been pulled from the worldometer website
  
Updated Scraped_Data.json file contains the dictionary with multiple days' data.
The dictionary is keyed with [Date][Country Name][Data Type]
For example, dated_dict["2022-11-28"]["China"]["Total Deaths"] will output the total deaths value for China on Nov. 28, 2022
  
RUNNING SCRAPEWEBSITE INSTRUCTIONS:

Download and save the ScrapeWebsite.py file to the project directory.
The file can be run as a script, which will default to running the scrape_website function (with worldometer as the default website). 
The file can also be used as a module to call any of the functions from another script. 
  
The saved json data files will be located in the same directory.
These files included dated backup files as well as a Scraped_Data.json file which contains several days of data.
The data is organized in a dictionary with nested keys of date, country (or world), and data type. 

RUNNING DASHBOARD INSTRUCTIONS:
To run dashboard navigate to directory in cmd then run : "python -m bokeh serve --show CovidDashboard.py"

NOTE: Some statistics were not available for data scraping so plots may not be available for specific dates.

