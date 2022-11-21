import json

json_file = open("Scraped_Data")

dict_dated = json.load(json_file) 

print(dict_dated["2022-11-21"]["China"])
print(dict_dated["2022-11-21"]["China"]["Total Cases"])


