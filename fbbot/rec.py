from flask import Flask, request
import json
import requests
import os
from scripts.ack import insertRec
import subprocess

VERIFY_TOKEN = "my_voice_is_my_pass_verify_me"
PAT = 'Enter your own FB Messenger Access Token Here'

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # Once the endpoint is added as a webhook, it must return back
    # the 'hub.challenge' value it receives in the request arguments
    if (request.args.get('hub.verify_token', '') == VERIFY_TOKEN):
        print("Verified")
        return request.args.get('hub.challenge', '')
    else:
        print('wrong verification token')
        return "Error, Verification Failed"
        
@app.route('/', methods=['POST'])
def handle_messages():
    data = request.get_json()
    entry = data['entry'][0]
    #print(data)
    if entry.get("messaging"):
        messaging_event = entry['messaging'][0]
        sender_id = messaging_event['sender']['id']
        timestamp = entry['time']
        print("Sender:",sender_id)
        if messaging_event.get("message"):
            if messaging_event['message'].get('quick_reply'):
                text = messaging_event['message']['quick_reply']['payload']
                #print("Payload:",text)
                insret = insertRec("db/rec.db","ack",sender_id,text,timestamp,0)
            else:
                if messaging_event['message'].get('text'):
                    text = messaging_event['message']['text']
                    #print("Message, Text:", text)
                    insret = insertRec("db/rec.db","ack",sender_id,text,timestamp,0)
                    return 'ok', 200
                if messaging_event['message'].get('sticker_id'):
                    if str(messaging_event['message']['sticker_id']) == str(369239263222822):
                        insret = insertRec("db/rec.db","ack",sender_id,"*box20",timestamp,0)
                        return 'ok', 200
                    elif str(messaging_event['message']['sticker_id']) == str(369239343222814):
                        insret = insertRec("db/rec.db","ack",sender_id,"*box10",timestamp,0)
                        return 'ok', 200
                    elif str(messaging_event['message']['sticker_id']) == str(369239383222810):
                        insret = insertRec("db/rec.db","ack",sender_id,"*box5",timestamp,0)
                        return 'ok', 200
                    return 'ok', 200
            return 'ok', 200
        elif messaging_event.get("postback"):
            if messaging_event['postback'].get('payload'):
                payload = messaging_event['postback']['payload']
                print("Payload:",payload)
                insret = insertRec("db/rec.db","ack",sender_id,payload,timestamp,0)
                return 'ok', 200
            return 'ok', 200
        else:
            print(messaging_event)
            return 'ok', 200
    return 'ok', 200
    
if __name__ == '__main__':
    subprocess.Popen("python3 ./res.py", shell=True)
    app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)))
    #app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080)),debug=True)