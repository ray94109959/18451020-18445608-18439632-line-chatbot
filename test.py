from __future__ import unicode_literals

import redis
import json
import urllib
import urllib.request

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

