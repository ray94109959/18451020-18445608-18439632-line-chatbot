from __future__ import unicode_literals

import os
import sys
import redis
import json
import urllib.request
import urllib.parse

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, FileMessage, StickerMessage, StickerSendMessage
)
from linebot.utils import PY3

HOST = "redis-18040.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
PWD = "xmiprQJOCm4tKebf8zbudmXt9I99fiRV"
PORT = "18040" 

redis1 = redis.Redis(host = HOST, password = PWD, port = PORT)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'

# Handler function for Text Message
def handle_TextMessage(event):
    print(event.message.text)
    msg = ''
    #msg = 'You said: "' + event.message.text + '" '
    
    txt = event.message.text.strip().upper()
    if txt == 'HI' or txt == '0' or txt == '你好' or txt =='喂' or txt=='YO' or txt=='HALO' or txt=='HEY' or txt=='HELLO' or txt=='早晨':
        msg = "Hi again, it is Corona, your Novel-Coronavirus Service Ambassador. I can help to answer general inquiries about COVID-19!"
    elif txt == '1':
        #msg = "Sorry, I'm not sure if I can help with that and still under the learning process. Your conversation with COVID-19 may be recorded for training, quality control and dispute handling purposes. Thanks!!"
        msg = "Face Mask information:\n"
        msg = msg + "\nAs of: " + redis1.get('last_udpated').decode('UTF-8') +"\n"

        for count in range(5):
            id = "mask:"+str(count)
            msg  = msg + "\n" + redis1.hmget(id,"name")[0].decode('UTF-8')
            msg  = msg + "\n" + redis1.hmget(id,"des")[0].decode('UTF-8') + "\n"
            # msg  = msg + "\n" + redis1.hmget(id,"url")[0].decode('UTF-8') 
        msg = msg + "\nSource: " + redis1.get('source_url').decode('UTF-8') 
         
    elif txt == '2':
        #url = 'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_wuhan_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D' 
        url = "https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Flatest_situation_of_reported_cases_covid_19_eng.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%7D"
        operUrl = urllib.request.urlopen(url)
        if(operUrl.getcode()==200):
            data = operUrl.read().decode()
            obj = json.loads(data)
            last = len(obj)-1
            previous = last - 1
            msg = "Latest situation of reported cases of COVID-19 in Hong Kong:\n"

            # msg = msg + str(obj[last]).replace("[","").replace("]","").replace("{","").replace("}","").replace('"',"").replace("'","").replace("\\n"," ").replace(", ","\n").replace("Number of ","").replace("ruled out cases: \n","").replace("cases still hospitalised for investigation: \n","").replace("cases fulfilling the reporting criteria: \n","")

            msg = msg + "\nAs of: " + obj[last]['As of date'] + " " + obj[last]['As of time'] 
            
            item = "Number of confirmed cases"
            msg = msg + "\nConfirmed cases #: " + str(obj[last][item]) 
            change = obj[last][item] - obj[previous][item] 
            if change > 0:
                msg = msg + " (+" + str(change) + ")"
            elif change < 0:
                msg = msg + " (" + str(change) + ")"

            item = "Number of death cases"
            msg = msg + "\nDeath cases #: " + str(obj[last][item]) 
            change = obj[last][item] - obj[previous][item] 
            if change > 0:
                msg = msg + " (+" + str(change) + ")"
            elif change < 0:
                msg = msg + " (" + str(change) + ")"    
            
            item = "Number of discharge cases"
            msg = msg + "\nDischarge cases #: " + str(obj[last][item]) 
            change = obj[last][item] - obj[previous][item] 
            if change > 0:
                msg = msg + " (+" + str(change) + ")"
            elif change < 0:
                msg = msg + " (" + str(change) + ")"    
            
            item = "Number of probable cases"
            msg = msg + "\nProbable cases #: " + str(obj[last][item]) 
            change = obj[last][item] - obj[previous][item] 
            if change > 0:
                msg = msg + " (+" + str(change) + ")"
            elif change < 0:
                msg = msg + " (" + str(change) + ")"    
            
            item = "Number of hospitalised cases in critical condition"
            msg = msg + "\nCritical cases #: " + str(obj[last][item]) 
            change = obj[last][item] - obj[previous][item] 
            if change > 0:
                msg = msg + " (+" + str(change) + ")"
            elif change < 0:
                msg = msg + " (" + str(change) + ")"    
            
            msg = msg + "\n\nSource: https://data.gov.hk/en-data/dataset/hk-dh-chpsebcddr-novel-infectious-agent"
        else:
            msg = "Server is busy, please try again later....."   
    elif txt == '3':
        msg = "Please play the video to watch health tips as below:\n"
        msg = msg + redis1.get('health_tips').decode('UTF-8')
    else:    
        param = urllib.parse.quote(txt)
        url = 'https://api.data.gov.hk/v2/filter?q=%7B%22resource%22%3A%22http%3A%2F%2Fwww.chp.gov.hk%2Ffiles%2Fmisc%2Fhome_confinees_tier2_building_list.csv%22%2C%22section%22%3A1%2C%22format%22%3A%22json%22%2C%22filters%22%3A%5B%5B3%2C%22ct%22%2C%5B%22'+param+'%22%5D%5D%5D%7D'
        operUrl = urllib.request.urlopen(url)
        if(operUrl.getcode()==200):
            data = operUrl.read().decode()
            obj = json.loads(data)
           
            if len(obj)>0:
                msg = "List of buildings of the home confinees under mandatory home quarantine according to Cap. 599C of Hong Kong Laws:\n"

                count = 0
                for location in obj:
                    msg = msg + "\nEnd Date: " + location["家居檢疫最後日期 End Date of Home Quarantine Order"] + "\n" + location["地址 Address"] + "\n"
                    count = count + 1
                    if  count >= 10:
                        break

                msg = msg + "\nSource: https://data.gov.hk/en-data/dataset/hk-dh-chpsebcddr-novel-infectious-agent"
            else:
                msg = "Sorry, no results found with '"+ event.message.text +"'."    
        else:
            msg = "Server is busy, please try again later....."  

    msg = msg + "\n\nCould you please tell me what are you looking for?\n1. Face Mask information\n2. Case in Hong Kong\n3. Health Tips\n\nKindly press 1, 2, 3\nOR\nInput building name/location for searching mandatory home quarantine (e.g. Central)"
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(msg)
    )

# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=event.message.package_id,
            sticker_id=event.message.sticker_id)
    )

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Sorry, I'm still learning the 'image' type question. At this moment, please kindly input text message as your question.")
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Sorry, I do not accept video now!")
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Sorry, I do not accept file now!")
    )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)