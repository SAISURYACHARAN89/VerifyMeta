from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import requests
import json

app = FastAPI()

VERIFY_TOKEN = "tricher_verify_token"
PAGE_TOKEN = "EAANKvOrEB0cBQ0DUhLVitbEV310PqmsV28kmynzs9APCthwpvHrXjv6eBZA7sQqjZBZCx97j4DwrMpbMjCnzHnZANqhqg8ZC6f2LeRDlZARmiQpfIHoMtTm10IMO5fyS1qQOOHZCyUZBq5hj3yXHrmpwL8JnKMW46SZCBpsTx8NGYp6K5ThlJRxfSz076o0fNweFdJmBfQZB2lWOvg37tJ4NZCnudKZBNPZABXGBGj8cUtWCzkJ4JIwNKZAAkhoIN1xHZB0EgQus5eAZCnp8NhTE04iKelK6OVCoEUpo4qrArlnfywZDZD"

# webhook verification
@app.get("/instagram/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


# function to send message
def send_message(user_id, text):

    url = "https://graph.facebook.com/v19.0/me/messages"

    headers = {
        "Authorization": f"Bearer {PAGE_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "recipient": {"id": user_id},
        "message": {"text": text}
    }

    r = requests.post(url, headers=headers, json=payload)

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
