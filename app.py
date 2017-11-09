import os
import sys
import json
from datetime import datetime
from watson_developer_cloud import *
import process
import stock
import random
import retirement
from watson_developer_cloud import *

import requests
from flask import Flask, request

app = Flask(__name__)

USERNAME = "17f9272a-a613-4cd4-b4a2-d2997333d8e3"
PASSWORD = "lTzpYkbjTsKE"
WORKSPACE_ID = "a347dca1-629e-4bbb-af35-d51aae52bf7a"
context = {}
r = {"complete": False}

conversation = conversation_v1.ConversationV1(
    username=USERNAME,
    password=PASSWORD,
    version='2016-06-20'
)


@app.route('/', methods=['GET'])
def verify():
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == os.environ["VERIFY_TOKEN"]:
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():
    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                print('###########################################')
                if messaging_event.get("message"):  # someone sent us a message
                    global context
                    sender_id = messaging_event["sender"]["id"]  # the facebook ID of the person sending you the message
                    recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                    message_text = messaging_event["message"]["text"]  # the message's text
                    newJSON, context = process.handle_command(message_text, context, conversation)
                    message = ''
                    #print(newJSON)
                    print(json.dumps(newJSON, indent=2))
                    print(newJSON['intents'][0]['intent'])
                    print(newJSON['output']['text'][0])
                    if (message_text.isdigit()):
                        message_text = int(message_text)
                    if (newJSON['intents'][0]['intent'] == 'Stock_Price' and newJSON['output']['text'][0] == 'INTENT'):
                        message = stock.getstockprice(newJSON['entities'][0]['value'])
                        send_message(sender_id, message)
                    elif (newJSON['intents'][0]['intent'] == 'Advice' and newJSON['output']['text'][0] == 'INTENT'):
                        f = open("InvestmentTips.txt", "r")
                        file = f.readlines()
                        rr = int(random.random() * 300)
                        send_message(sender_id, "investment tip #%s" % (file[rr]))
                        f.close()
                    elif message_text == "test":
                        send_message(sender_id, "test success!")
                    elif (newJSON['intents'][0]['intent'] == u'Save_For_Retirement'):
                        r.update({"retire": True})
                        send_message(sender_id, "When do you want to retire?")
                    elif (newJSON['output']['text'][0] == u'How old are you right now?'):
                        r.update({"ageRetire": newJSON['context']['age']})
                        send_message(sender_id, newJSON['output']['text'][0])
                    elif (newJSON['output']['text'][0] == u'How much money do you have saved up?'):
                        r.update({"ageNow": newJSON['context']['age']})
                        send_message(sender_id, newJSON['output']['text'][0])
                    elif (newJSON['output']['text'][0] == u"What's your current income?"):
                        r.update({"savings": newJSON['context']['age']})
                        send_message(sender_id, newJSON['output']['text'][0])
                    elif (newJSON['output']['text'][0] == u'What is up my dude'):
                        r.update({"incomeCurrent": newJSON['context']['age']})
                        r.update({"complete": True})
                        x, y = retirement.calculate(r['ageNow'], r['ageRetire'], r['incomeCurrent'], r['savings'])
                        r["complete"] = False
                        send_message(sender_id,
                                     "If you save the recommended 10%% of your income every year, you will retire with $%d, which will last you %d years!" % (
                                     x, y))
                    else:
                        send_message(sender_id, newJSON['output']['text'][0])

    return "ok", 200


def send_message(recipient_id, message_text):
    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            msg = unicode(msg).format(*args, **kwargs)
        print
        u"{}: {}".format(datetime.now(), msg)
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)