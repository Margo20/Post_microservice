import base64
import os
import logging
from fastapi import FastAPI, HTTPException
from pydantic.main import BaseModel
from celery_worker import send_mail
from hash_password import fastapi_crypt_pass

salt_bytes = base64.b64decode(os.getenv('SALT_BASE64').encode())
hash_bytes = base64.b64decode(os.getenv('HASH_BASE64').encode())


class Msg(BaseModel):
    email_address: str
    password: str

api = FastAPI()

@api.post("/my_send_email")
async def enqueue_add(msg: Msg):
    logging.info("New message: %s" % (msg.email_address))
    hash_from_clients = fastapi_crypt_pass(msg.password, salt_bytes)

    if hash_from_clients==hash_bytes:
        send_mail.delay(msg.dict())
    else:
        logging.warning("Password not valid")
        raise HTTPException(status_code=401, detail="wrong password")
