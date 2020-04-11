from __future__ import unicode_literals

import redis


# For connection to redis.

HOST = "redis-18040.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
PWD = "xmiprQJOCm4tKebf8zbudmXt9I99fiRV"
PORT = "18040" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)


while True:
    # url = 'https://youtu.be/FXBaQb8RHjI'
    url = 'https://youtu.be/J0FbVrwGYUQ'
    msg = input("Please enter video url to update health tips (default youtube video if empty, type 'q' to end):").strip()
    if msg == 'quit' or msg == 'exit' or msg == "q":
        break
    if msg == '':
        msg = url
    print("You have entered " + msg, end='\n') 

   
    # Add video url to redis
    redis1.set('health_tips', msg)
    
    # print(redis1.get('health_tips'))
    # print(redis1.get('health_tips').decode('UTF-8'))


