import re
import pycurl
from io import BytesIO 


b_obj = BytesIO() 
crl = pycurl.Curl() 

# Set URL value
#crl.setopt(crl.URL, 'https://wiki.python.org/moin/BeginnersGuide')
crl.setopt(crl.URL, 'https://sme.hket.com/article/2555326/')

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

s = get_body.decode('utf8')

#print re.match(r'<.*?>', s).group()
# pat = re.compile(r"\s*(?P<header>[^:]+)\s*:(?P<value>.*?)\s*$")
# print(pat)

html_body = get_body.decode('utf8')

something = re.findall(r"\<p><strong>(.*)<\/strong><\/p>", html_body)
somethingelse = re.findall(r"\<p>(.*)<a href=\"(.*)\" .*>\u8a73\u60c5<\/a><\/p>", html_body)

# print (somethingelse)
count = 0
for result in somethingelse:
    print (result)
    count = count + 1
    if  count >= 5:
        break

count = 0
for result in something:
    print (result)
    count = count + 1
    if  count >= 5:
        break
