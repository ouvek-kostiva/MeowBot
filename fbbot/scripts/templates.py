import requests
import json
import os
from requests_toolbelt.multipart.encoder import MultipartEncoder

PAT = 'Enter your own FB Messenger Access Token Here'

def send_text_message(recipient_id, message):
    #print("Respond to User:",recipient_id,"Text:",message)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {"text": message}
    })
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
    #print(r)
                      
def send_img_message(recipient_id,fileName):
    data = {
        "recipient": json.dumps({
            "id": recipient_id
        }),
        "message": json.dumps({
            "attachment": {
                "type": "image",
                'payload': {}
            }
        }),
        'filedata': (os.path.basename(fileName), open(fileName, 'rb'), 'image/png')
    }
    multipart_data = MultipartEncoder(data)
    multipart_header = {
        'Content-Type': multipart_data.content_type
    }
    params = {
        "access_token": PAT
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=multipart_header, data=multipart_data)
                      
def send_pfquikreply_message(recipient_id, message):
    #print("Respond to User:",recipient_id,"Text:",message)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "text": message,
            "quick_replies": [
                {"content_type":"text",
                 "title":"*1",
                 "payload":"*1"},
                 {"content_type":"text",
                 "title":"*2",
                 "payload":"*2"},
                 {"content_type":"text",
                 "title":"*3",
                 "payload":"*3"},
                 {"content_type":"text",
                 "title":"*4",
                 "payload":"*4"},
                 {"content_type":"text",
                 "title":"*5",
                 "payload":"*5"},
                 {"content_type":"text",
                 "title":"*6",
                 "payload":"*6"},
                 {"content_type":"text",
                 "title":"*7",
                 "payload":"*7"},
                 {"content_type":"text",
                 "title":"*8",
                 "payload":"*8"},
                 {"content_type":"text",
                 "title":"*9",
                 "payload":"*9"},
                 {"content_type":"text",
                 "title":"*10",
                 "payload":"*10"}
            ]
        }
    })
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
                      
def send_boxquikreply_message(recipient_id, message):
    #print("Respond to User:",recipient_id,"Text:",message)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "text": message,
            "quick_replies": [
                {"content_type":"text",
                 "title":"抽 1 寶箱",
                 "payload":"*box"},
                 {"content_type":"text",
                 "title":"抽 5 寶箱",
                 "payload":"*box5"},
                 {"content_type":"text",
                 "title":"抽 10 寶箱",
                 "payload":"*box10"},
                 {"content_type":"text",
                 "title":"抽 15 寶箱",
                 "payload":"*box15"},
                 {"content_type":"text",
                 "title":"抽 20 寶箱",
                 "payload":"*box20"}
            ]
        }
    })
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
                      
def send_stockquikreply_message(recipient_id, message):
    #print("Respond to User:",recipient_id,"Text:",message)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "text": message,
            "quick_replies": [
                {"content_type":"text",
                 "title":"財務健檢",
                 "payload":"*fh"},
                 {"content_type":"text",
                 "title":"趨勢預測",
                 "payload":"*pp"}
            ]
        }
    })
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)
                      
def send_funcquikreply_message(recipient_id, message):
    #print("Respond to User:",recipient_id,"Text:",message)
    data = json.dumps({
        "recipient": {"id": recipient_id},
        "message": {
            "text": message,
            "quick_replies": [
                {"content_type":"text",
                 "title":"理財知識",
                 "payload":"*pf"},
                 {"content_type":"text",
                 "title":"抽寶箱",
                 "payload":"*bq"},
                 {"content_type":"text",
                 "title":"目前擁有點數與每日獎勵",
                 "payload":"*daily"}
            ]
        }
    })
    params = {
        "access_token": PAT
    }
    headers = {
        "Content-Type": "application/json"
    }
    r = requests.post("https://graph.facebook.com/v2.6/me/messages",
                      params=params, headers=headers, data=data)