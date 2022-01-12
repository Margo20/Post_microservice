from fastapi import FastAPI
from pydantic.main import BaseModel
from celery_worker import send_mail

class Msg(BaseModel):
    email_address: str

api = FastAPI()

@api.post("/my_send_email")
async def enqueue_add(msg: Msg):
    print(msg.email_address)
    send_mail.delay(msg.dict())
