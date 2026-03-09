from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import json

app = FastAPI()

VERIFY_TOKEN = "tricher_verify_token"
PAGE_TOKEN = "IGAALPXhZAsCzhBZAFlEMjd4bktnc0NsY2o1a1V5ZA2VCOThBX0VUYlRZAcHo4OTExd3MxUDJhM2duMUpRUTE4WjF2VXFQb2NZAUVVNOVBoM3FMQ0ZApUks2UmY0S0RqaFVaTmpicFVvMU9ONTRsd2pMMzVId18xMkUzZAGxLRGNIeV9GdwZDZD"

# webhook verification
@app.get("/instagram/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


def send_message(user_id, text):

    url = "https://graph.facebook.com/v19.0/17841479663844392/messages"

    params = {
        "access_token": PAGE_TOKEN
    }

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    r = requests.post(url, params=params, json=payload)

    print("Send response:", r.text)

# webhook receiver
@app.post("/instagram/webhook")
async def receive_webhook(request: Request):

    body = await request.body()
    data = json.loads(body)

    print("📩 Webhook received:", data)

    for entry in data.get("entry", []):
        for msg in entry.get("messaging", []):

            sender_id = msg["sender"]["id"]

            if "message" in msg and "text" in msg["message"]:
                text = msg["message"]["text"]

                print("User said:", text)

                send_message(sender_id, "Hello! 👋 Thanks for messaging Tricher. How can I help you?")

    return {"status": "ok"}
