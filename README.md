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
The ImportScrapedData script is a script to test functionality for importing the data from a saved file to be used elsewhere.
