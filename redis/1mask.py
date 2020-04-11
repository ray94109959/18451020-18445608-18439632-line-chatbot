import redis
import html
import re
import pycurl
from io import BytesIO 

HOST = "redis-18040.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
PWD = "xmiprQJOCm4tKebf8zbudmXt9I99fiRV"
PORT = "18040" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)

b_obj = BytesIO() 
crl = pycurl.Curl() 

# Set URL value
#crl.setopt(crl.URL, 'https://wiki.python.org/moin/BeginnersGuide')
source = "https://sme.hket.com/article/2555326"
crl.setopt(crl.URL, source)

# Write bytes that are utf-8 encoded
crl.setopt(crl.WRITEDATA, b_obj)

# Perform a file transfer 
crl.perform() 

# End curl session
crl.close()

# Get the content stored in the BytesIO object (in byte characters) 
get_body = b_obj.getvalue()

# Decode the bytes stored in get_body to HTML and print the result 
# print('Output of GET request:\n%s' % get_body.decode('utf8')) 

html_body = get_body.decode('utf8')

#print re.match(r'<.*?>', s).group()
# pat = re.compile(r"\s*(?P<header>[^:]+)\s*:(?P<value>.*?)\s*$")
# print(pat)


# shop = re.findall(r"\<p><strong>(.*)<\/strong><\/p>", html_body)
# news = re.findall(r"\<p>(.*)<a href=\"(.*)\" .*>\u8a73\u60c5<\/a><\/p>", html_body)
news = re.findall(r"<p>(.*)<\/p>\n\n\<p>(.*)<a href=\"(.*)\" .*>\u8a73\u60c5<\/a><\/p>", html_body)
time = re.findall(r"<span class=\"article-details-info-container_date\">\n.*<span class=\"font-en\">(.*)<\/span>\n.*<span class=\"font-en\">(.*)<\/span>", html_body)

last = time[0][1] + " " + time[0][0]

redis1.set('source_url', source)
redis1.set('last_udpated', last)

print(redis1.get('source_url').decode('UTF-8'))
print(redis1.get('last_udpated').decode('UTF-8'))

count = 0
for result in news:
   
    mask = {
        "name": html.unescape(result[0].replace("<strong>","").replace("</strong>","")),
        "des": html.unescape(result[1]),
        "url": result[2]
    }

    id = "mask:"+str(count)
    redis1.hmset(id, mask)
    items = redis1.hgetall(id)
    name = redis1.hmget(id,"name")[0].decode('UTF-8')
    des = redis1.hmget(id,"des")[0].decode('UTF-8')
    url = redis1.hmget(id,"url")[0].decode('UTF-8')
    print(id)
    print(name)
    print(des)
    print(url)

    count = count + 1
    if  count >= 10:
        break


