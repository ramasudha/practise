import csv
import json
import pprint
 

city_names = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Kolkata"]
city_ids = []
with open("D:\\ram\\python_wheather\\city_list1.json", 'r') as f:
    data = json.load(f)
    #pprint.pprint(data)
    for city in city_names:
       for d in data:
           if d["country"] == "IN" and d["name"] == city:
               ids = city_ids.append(d["id"])
    
    #pprint.pprint(data)


#with open(r'D:\ram\python_wheather\city_list1.json', 'r') as f:
#    data = json.load(f)
#    for city in city_names:
#        for d in data:
#            if d["country"] == "IN" and d["name"] == city:
#                ids = city_ids.append(d["id"])
print(city_ids)

    # print(data)
