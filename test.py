from __future__ import unicode_literals

import redis
import json
import urllib
import urllib.request
import urllib.parse

# fill in the following.
# HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
# PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
# PORT = "11363" 
HOST = "redis-18040.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
PWD = "xmiprQJOCm4tKebf8zbudmXt9I99fiRV"
PORT = "18040" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)


while True:
    msg = input("Please enter your query (type 'quit' or 'exit' to end):").strip()
    if msg == 'quit' or msg == 'exit':
        break
    if msg == '':
        continue
    print("You have entered " + msg, end=' ') 

   
    # Add your code here
    
    count = 0
    if redis1.get(msg):
        count = int(redis1.get(msg))
    

    value = 1 + count
    redis1.set(msg, value)

    print('for '+ str(value) +' times' )
    
    if msg == '2':
        print(" 2222222 " + msg, end=' ') 
    # a Python object (dict):
    x = {
    "name": "John",
    "age": 30,
    "city": "New York"
    }

    # convert into JSON:
    y = json.dumps(x)

    # the result is a JSON string:
    print(y)

    url = 'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_wuhan_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D' 
   
    data = urllib.request.urlopen(url).read().decode()
    obj = json.loads(data)
    last = len(obj)-1

    print(obj[last])
    print(obj[last]['Number of confirmed cases'])


    #param = '%E8%A5%BF%E7%92%B0'
    search = "西環"
    print(search)
    param = urllib.parse.quote(search)
    print(param)
    #url = 'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fhome_confinees_tier2_building_list.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B3%2C%22ct%22%2C%5B%22%E8%A5%BF%E7%92%B0%22%5D%5D%5D%7D'
    url = 'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fhome_confinees_tier2_building_list.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B3%2C%22ct%22%2C%5B%22'+param+'%22%5D%5D%5D%7D'
    
    operUrl = urllib.request.urlopen(url)
    if(operUrl.getcode()==200):
        data = operUrl.read().decode()
        obj = json.loads(data)
        
        msg = "List of buildings of the home confinees under mandatory home quarantine according to Cap. 599C of Hong Kong Laws\n\n"

        report = str(obj) 
        #.replace("'","").replace("{","").replace("}","").replace(", ","\n")
        msg = msg + report 
    else:
        msg = "Server is busy, please try again later....."  

    print(msg)    

