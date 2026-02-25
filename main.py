from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
import os

app = FastAPI()

VERIFY_TOKEN = "tricher_verify_token"

# 1️⃣ Verification endpoint
@app.get("/instagram/webhook")
async def verify_webhook(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return PlainTextResponse(challenge)

    return PlainTextResponse("Verification failed", status_code=403)


# 2️⃣ Receive messages
@app.post("/instagram/webhook")
async def receive_webhook(request: Request):
    data = await request.json()
    print("Webhook received:", data)
    return {"status": "ok"}