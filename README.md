# Covid_Dashboard_MEEN6250

Yousef Alsanea

Anthony Lew

ME EN 6250

University of Utah

Course Project

11 Dec 2022


Covid Dashboard Project for ME EN 6250 course

This project will scrape data from a Covid death tracking website to be used in a graphical dashboard interface


The ScrapeWebsiteScript is a script to test functionality for the module that will be developed. 
This uses the json, requests, bs4, datetime, and os python libraries.
The script is set up toe read from the worldometer.info/coronavirus website.
The script pulls country names and total and new data for cases and deaths (in absolute and per 1 million).
A dictionary is created from this data with nested keys starting with day (yyyy-mm-dd string format), country name (or "World") and then data type ("Total Cases" or "New Deaths /1M"). 
Each new day is appended to the dictionary in the json file (or a new file is created if a json does not already exist).
Each day's dictionary is also saved as it's own json file for backup, named "<date>.json" (2022-11-21.json).
 
The ImportScrapedData script is a script to test functionality for importing the data from a saved file to be used elsewhere and the functions called from the imported ScrapeWebsite module.

The module ScrapeWebsite.py has been added.
This module includes functions:
scrape_website -- to pull data from a website and save the days data to a backup file and append the data to the Scraped_Data.json file
scrape_country -- to pull a single country's data from a website for today
append_date -- to arbitrarily add a day's data to the Scraped_Data.json given the data has already been stored as a dated backup file
  
Dated .json files contain dictionaries with the data from previous days that have been pulled from the worldometer website
  
Updated Scraped_Data.json file contains the dictionary with multiple days' data.
The dictionary is keyed with [Date][Country Name][Data Type]
For example, dated_dict["2022-11-28"]["China"]["Total Deaths"] will output the total deaths value for China on Nov. 28, 2022
