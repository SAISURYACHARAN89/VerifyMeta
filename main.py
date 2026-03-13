from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import json

app = FastAPI()

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

VERIFY_TOKEN = "tricher_verify_token"

PAGE_TOKEN = "EAANKvOrEB0cBQyuIyhtHaBaPBQJVT0Fw4hir0WoJu1eWnFaoa68xLZCyyLvAO2ZCMn1GuQXFgy87dSGhzd9kDZAHWTUK9ZA75wEHiqopo1tF5T9zZBZCtJ5L4Qxu5341VW9pV1NBZCMP9wNSdmcU4Fug7C5p9wktkFgT2nZCZCEFMZA0V5GVNu5jAMGbBu4AZCFlhqJtnE5oDHrh638ZAydQHkD60ojHJHUG5F4Qv57loR5rsntssQNIqTe8judm"

messages = []
last_user = None


# =========================
# webhook verification
# =========================
@app.get("/instagram/webhook")
async def verify_webhook(request: Request):

    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


# =========================
# send message
# =========================
def send_message(user_id, text):

    url = "https://graph.facebook.com/v19.0/me/messages"

    params = {
        "access_token": PAGE_TOKEN
    }

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    r = requests.post(url, params=params, json=payload)

    print("Send response:", r.text)


# =========================
# webhook receiver
# =========================
@app.post("/instagram/webhook")
async def receive_webhook(request: Request):

    global last_user

    body = await request.body()
    data = json.loads(body)

    print("Webhook:", data)

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):

            sender_id = msg["sender"]["id"]
            last_user = sender_id

            if "message" in msg and "text" in msg["message"]:

                text = msg["message"]["text"]

                messages.append({
                    "from": "user",
                    "text": text
                })

    return {"status": "ok"}


# =========================
# get messages
# =========================
@app.get("/messages")
def get_messages():
    return messages


# =========================
# send reply
# =========================
@app.post("/send")
async def send_reply(request: Request):

    global last_user

    data = await request.json()

    text = data["text"]

    if last_user:

        send_message(last_user, text)

        messages.append({
            "from": "me",
            "text": text
        })

    return {"ok": True}
