import json
import requests
import bs4
import datetime
import os

response = requests.get("https://www.worldometers.info/coronavirus/#countries")

soup = bs4.BeautifulSoup(response.content, "html.parser")

#print(response.content)

site_data = soup.find_all("td")

#print(site_data)
#print(site_data[177:180])

i = 155
data_dict = {}

for index in range(231):
    if i == 155:
        country_name = "World"
    else:
        country_html = str(site_data[i])
        end_char = -6
        while country_html[end_char] != "<":
            end_char += -1
        start_char = end_char
        while country_html[start_char] != ">":
            start_char += -1
        country_name = country_html[start_char+1:end_char]

    data_list = []
    for ii in range(21):
        data_html = str(site_data[i+ii+1])
        if i == 155:
            start_char = 4
            end_char = -5
        else:
            end_char = -5
            start_char = end_char
            while data_html[start_char] != ">":
                start_char += -1
        data_value = data_html[start_char+1:end_char]
        data_value_nc = data_value.replace(",","")
        data_value_ns = data_value_nc.replace(" ","")
        data_value_np = data_value_ns.replace("+","")
        if data_value_np == "":
            input_data = "N/A"
        elif data_value_np[0].isdigit():
            input_data = float(data_value_np)
        else:
            input_data = data_value
        data_list.append(input_data)
    i += 22

    data_dict[country_name] = {\
        "Total Cases":data_list[0],\
        "New Cases":data_list[1],\
        "Total Deaths":data_list[2],\
        "New Deaths":data_list[3],\
        "Total Cases /1M":data_list[8],\
        "New Cases /1M":data_list[9],\
        "Total Deaths /1M":data_list[17],\
        "New Deaths /1M":data_list[18]}

#print(country_name)
#print(data_list)
    
print(f"South Korea data: {data_dict['S. Korea']}")

#######################################################################################
today_date_obj = datetime.datetime.now(datetime.timezone.utc)
today_date = str(today_date_obj.date())
with open(today_date, "w") as json_file_i:
    json.dump(data_dict , json_file_i, indent = 4)

if not os.path.isfile("Scraped_Data"):
    dict_dated = {today_date:data_dict}
    with open("Scraped_Data", "w") as json_file:
        json.dump(dict_dated , json_file, indent = 4) 
else:
    json_file_old = open("Scraped_Data")
    dict_dated = json.load(json_file_old) 
    dict_dated[today_date] = data_dict
    with open("Scraped_Data", "w") as json_file:
        json.dump(dict_dated , json_file, indent = 4) 

###########################################################################################



#Data Structure:
#var columns = {\n            
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