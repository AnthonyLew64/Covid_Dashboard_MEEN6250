import json
import requests
import bs4
import datetime
import os

#This module was created by:
#Yousef Alsanea and Anthony Lew
#The most recent update to this module was completed on:
#2022-11-28
#This module was created to fulfill the requirements of a project in the
#ME EN 6250 course, "Programming for Engineers," at the University of Utah, taught by
#Dr. Daniel Balouek-Thomert

def scrape_website(site_address = "https://www.worldometers.info/coronavirus/#countries"):
    """
    This function will scrape data from the website input into the site_address string
    This function can only handle websites that are formatted exactly as the worldometer coronavirus tracker:
    "https://www.worldometers.info/coronavirus/#countries"
    The scraped data for today is saved as a .json file with the date as its name (YYYY-MM-DD.json)
    The function will also create a new data file named Scraped_Data.json to save multiple days of data
    If this file already exists, the newly scraped data will be appended into this file
    The json file stores the data as a dictionary with nested keys:
    date, country, data_type
    For example:
    dict_dated["2022-11-28"]["S. Korea"]["Total Deaths"]
    will output the total death count for South Korea on November 28, 2022
    This function requires the json, requests, bs4, datetime, and os modules
    """
    #Check if the website passed to the function is worldometer
    if site_address == "https://www.worldometers.info/coronavirus/#countries":
        pass
    #If it is not, print a warning that the function is only formatted for worldometer
    else:
        print("Warning: Function is only able to handle websites formatted exactly like 'https://www.worldometers.info/coronavirus/#countries'")

    #Get data from the worldometer website using requests modules
    response = requests.get(site_address)

    #Uncomment to view the data from the website
    #print(response.content)

    #Format data using bs4 module
    soup = bs4.BeautifulSoup(response.content, "html.parser")

    #Use the bs4 soup class to select each element labelled "td"
    #All of the required data (country name, individual statistics) are collected under "td" in the website data
    site_data = soup.find_all("td")

    #Uncomment to view all of the "td" data or the data for one example country
    #print(site_data)
    #print(site_data[177:198])

    #Initialize variable, 155 is when the applicable data table begins
    #The data is formatted such that each country fills 22 lines of "td" data
    i = 155

    #Initialize Variable for the dictionary to collect the data
    data_dict = {}

    #This for loop iterates over each of the countries listed on the worldometer website
    #There are 230 countries and an entry for worldwide statistics, for a total of 231
    for index in range(231):
        #This if-else statement is used to assign a string with the country's name to the country_name variable
        if i == 155:
            #The entry for World is formatted differently, so the value is manually assigned here
            country_name = "World"
        else:
            #For every other country, first pull the string which includes the country name
            country_html = str(site_data[i])
            #For the formatting of the worldometer website, the end of the country names begin at position -6 in the string
            end_char = -6
            #To account for different country name lengths, "<" and ">" are used as delimiter characters
            #The while loops iterate until the beginning and end of the country name are found
            while country_html[end_char] != "<":
                end_char += -1
            start_char = end_char
            while country_html[start_char] != ">":
                start_char += -1
            #With the calculated start and end positions of the country name, the name can be assigned to the country_name variable
            country_name = country_html[start_char+1:end_char]
            #For countries with non-standard letters, replace the characters with letters
            country_name = country_name.replace("\u00e7","c")
            country_name = country_name.replace("\u00e9","e")

        #Initialize a variable to contain each countries data
        data_list = []
        #For loop to collect all of the data for each country
        #The data spans 22 lines (line 1 is the country name)
        for ii in range(21):
            #First pull the string with the required data
            #Index i refers to the country (assigned in the outer loop)
            #Index ii refers to the line of data (assigned in the inner loop)
            data_html = str(site_data[i+ii+1])
            #Each data value begins at position -5 in the string
            end_char = -5
            #Because world data is formatted differently, the starting character is assigned manually
            if i == 155:
                start_char = 4
            #For each other country
            else:
                #Initialize a varable for the beginning of the data value in the string
                start_char = end_char
                #Use a while loop to find the ">" delimiter position
                while data_html[start_char] != ">":
                    start_char += -1
            #With the computed start and end points, assign the string with the data value to the data_value variable
            data_value = data_html[start_char+1:end_char]
            #In order to convert to integer or float types, remove commas, spaces, and "+"
            data_value_nc = data_value.replace(",","")
            data_value_ns = data_value_nc.replace(" ","")
            data_value_np = data_value_ns.replace("+","")
            #If statement to handle different data types
            if data_value_np == "":
                #If there is no data listed, print "N/A"
                input_data = "N/A"
            elif data_value_np[0].isdigit():
                #If the data begins with a number (digit), assign it as a float
                input_data = float(data_value_np)
            else:
                #Otherwise, leave the data as a string
                input_data = data_value
            #Append the data to the data list variable
            data_list.append(input_data)

        #Assign a new key to the data_dict dictionary with outputs for each data type of interest
        data_dict[country_name] = {\
            "Total Cases":data_list[0],\
            "New Cases":data_list[1],\
            "Total Deaths":data_list[2],\
            "New Deaths":data_list[3],\
            "Total Cases /1M":data_list[8],\
            "New Cases /1M":data_list[9],\
            "Total Deaths /1M":data_list[17],\
            "New Deaths /1M":data_list[18]}
        
        #Add 22 to the index to continue to the next country
        i += 22

    #Uncomment to print an example of the dictionary entry 
    #print(f"South Korea data: {data_dict['S. Korea']}")

    #######################################################################################

    #Use the datetime module to compute today's date (to label the data)
    today_date_obj = datetime.datetime.now(datetime.timezone.utc)
    #Format the data as a string of YYYY-MM-DD
    today_date = str(today_date_obj.date())
    #Create a new file named YYYY-MM-DD.json with today's date
    with open(today_date+".json", "w") as json_file_i:
        #Write the data_dict dictionary to that file as a formatted json
        json.dump(data_dict , json_file_i, indent = 4)

    #Check if a file already exists for the compiled scrapped data
    #If the file does not already exist
    if not os.path.isfile("Scraped_Data.json"):
        #print("New File Created")
        #Create a new dictionary with a key of today's date corresponding to the dictionary of country data
        dict_dated = {today_date:data_dict}
        #Create a new file to write that data to
        with open("Scraped_Data.json", "w") as json_file:
            #Save the new dictionary to that file as a formatted json
            json.dump(dict_dated , json_file, indent = 4) 
    #If the file does already exist
    else:
        #print("New Data Appended to Existing File")
        #Open that existing file
        json_file_old = open("Scraped_Data.json")
        #Import the dictionary from that file
        dict_dated = json.load(json_file_old) 
        #Append the new data from today to that dictionary
        #Or update the data with the newly collected data if today's data is already present
        dict_dated[today_date] = data_dict
        #Open that file to replace the old data
        with open("Scraped_Data.json", "w") as json_file:
            #Save the new, updated dictionary to that file as a formatted json
            json.dump(dict_dated , json_file, indent = 4) 

    #######################################################################################

    #The following comment shows the data structure that is used in the table on the worldometer website
    #Data Structure:
    # var columns = {\n            
    # \'Total Cases\': 2,\n            
    # \'New Cases\': 3,\n            
    # \'Total Deaths\': 4,\n            
    # \'New Deaths\': 5,\n            
    # \'Total Recovered\': 6,\n            
    # \'New Recovered\': 7,\n            
    # \'Active Cases\': 8,\n            
    # \'Serious, Critical\': 9,\n            
    # \'Tot Cases/1M pop\': 10,\n            
    # \'Deaths/1M pop\': 11,\n            
    # \'Total Tests\': 12,\n            
    # \'Tests/1M pop\': 13,\n            
    # \'Population\': 14,\n\n            
    # \'1 Case every X ppl\': 16,\n            
    # \'1 Death every X ppl\': 17,\n            
    # \'1 Test every X ppl\': 18,\n\n            
    # \'New Cases/1M pop\': 19,\n            
    # \'New Deaths/1M pop\': 20,\n            
    # \'Active Cases/1M pop\': 21,\n        };
            
def scrape_country(country_name = "World", site_address = "https://www.worldometers.info/coronavirus/#countries"):
    """
    This function will call the scrape_website function for the input site address
    Then, it will output the data for the county specified in the country_name variable for today
    """
    #Check if the website passed to the function is worldometer
    if site_address == "https://www.worldometers.info/coronavirus/#countries":
        pass
    #If it is not, print a warning that the function is only formatted for worldometer
    else:
        print("Warning: Function is only able to handle websites formatted exactly like 'https://www.worldometers.info/coronavirus/#countries'")

    #Call the scrape website function to collect data
    scrape_website(site_address)
    #Use the datetime module to compute today's date (to label the data)
    today_date_obj = datetime.datetime.now(datetime.timezone.utc)
    #Format the data as a string of YYYY-MM-DD
    today_date = str(today_date_obj.date())
    #Open the file for today's data
    json_file = open(today_date+".json")
    #Load the saved dictionary for today's data
    data_dict = json.load(json_file)

    #Check if the input country exists in the file
    if country_name in data_dict.keys():
        pass
    else:
        #If not, print a warning and the valid country names
        print(f"Warning: the input country was not found in the data. Please select a valid country in {data_dict.keys()}")

    #Print the data for the selected country
    print(f"On {today_date}, {country_name} had: {data_dict[country_name]}")
    #Return that data to the function
    return data_dict[country_name]

def append_date(date_to_append):
    """
    This function will take the data from the date_to_append and will add it to the Scraped_Data.json file
    The data must already exist in a json file
    The Scraped_Data.json file must already exist for this function to append
    If this file has not been created yet, run the scrape_website function first
    The date_to_append variable requires a string formatted as YYYY-MM-DD.json (ex: "2022-11-21.json")
    """
    #Check if the Scraped_Data.json file has been created
    if os.path.isfile("Scraped_Data.json"):
        pass
    else:
        #If not, tell user that they must run the scrape_website function first
        print("Warning: The Scraped_Data.json file does not exist. Please run the scrape_website function first.")

    #Check if the data file for the input date exists
    if os.path.isfile(date_to_append+".json"):
        pass
    else:
        #If not, tell user that they must input a date that has a data file
        print("Warning: The selected date file does not exist. Please input a date that has an associated data file.")

    #Open the file with the selected day's data
    json_file = open(date_to_append+".json")
    #Load the saved dictionary for the selected day's data
    data_dict = json.load(json_file)
    #Open the scraped data file
    json_file_old = open("Scraped_Data.json")
    #Import the dictionary from that file
    dict_dated = json.load(json_file_old) 
    #Append the new data from today to that dictionary
    #Or update the data with the newly collected data if today's data is already present
    dict_dated[date_to_append] = data_dict
    #Open that file to replace the old data
    with open("Scraped_Data.json", "w") as json_file:
        #Save the new, updated dictionary to that file as a formatted json
        json.dump(dict_dated , json_file, indent = 4) 

#If the module is run as a script, call the scrape_website function
if __name__ == "__main__":
    scrape_website()

