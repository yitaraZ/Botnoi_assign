from flask import Flask, request, abort
import requests

app = Flask(__name__)

CHANNEL_ACCESS_TOKEN = "sCLZOGr0DcS0LfGCgYdt8oW3nkbNPRvHHAZrAFpKtzYOxeS3HBmvIoSQFOd9uECibyemzG0/eMFqvxsCQvEPD28uDppd6jTlO1xhziPJzqHNQgwYHFPtIPxHW71EuoAh7xP7oUMF7IRlcJp4TjsyLAdB04t89/1O/w1cDnyilFU="

def reply_message(reply_token, messages):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": messages
    }
    r = requests.post("https://api.line.me/v2/bot/message/reply", headers=headers, json=payload)
    return r.status_code

def create_quick_reply(reply_token):
    messages = [
        {
            "type": "text",
            "text": "Select an option:",
            "quickReply": {
                "items": [
                    {
                        "type": "action",
                        "action": {
                            "type": "message",
                            "label": "Yes",
                            "text": "Yes"
                        }
                    },
                    {
                        "type": "action",
                        "action": {
                            "type": "message",
                            "label": "No",
                            "text": "No"
                        }
                    }
                ]
            }
        }
    ]
    reply_message(reply_token, messages)

@app.route("/", methods=["POST", "GET"])
def callback():
    if request.method == "POST":
        payload = request.get_json()
        for event in payload["events"]:
            if event["type"] == "message" and event["message"]["type"] == "text":
                reply_token = event["replyToken"]
                message_text = event["message"]["text"]
                if message_text == "quick reply":
                    create_quick_reply(reply_token)
                else:
                    messages = [
                        {
                            "type": "text",
                            "text": "Hello, world!"
                        }
                    ]
                    reply_message(reply_token, messages)
        return "", 200
    else:
        return "Hello, World!"


if __name__ == "__main__":
    app.run(debug=True)
