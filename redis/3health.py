from __future__ import unicode_literals

import redis


# fill in the following.
# HOST = "redis-11363.c1.asia-northeast1-1.gce.cloud.redislabs.com"
# PWD = "1nOA0St0I7p9pQqu8HkQ18XqDfnoPeoL"
# PORT = "11363" 
HOST = "redis-18040.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
PWD = "xmiprQJOCm4tKebf8zbudmXt9I99fiRV"
PORT = "18040" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)


while True:
    url = 'https://youtu.be/FXBaQb8RHjI'
    msg = input("Please enter your health tips video url (default video if empty, type 'quit' or 'exit' to end):").strip()
    if msg == 'quit' or msg == 'exit':
        break
    if msg == '':
        msg = url
    print("You have entered " + msg, end='\n') 

   
    # Add your code here
    
 
    redis1.set('health_tips', msg)
    url = redis1.get('health_tips').decode('UTF-8')

    #print(url)

