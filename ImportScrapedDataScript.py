import json

json_file = open("Scraped_Data.json")

dict_dated = json.load(json_file) 

print(dict_dated["2022-11-22"]["China"])
print(dict_dated["2022-11-22"]["China"]["Total Cases"])
