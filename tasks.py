from celery import Celery
from celery import shared_task
from .consumer import receive
from main import send_mail

app = Celery("tasks", broker='redis://localhost:6379/0', backend='redis://localhost')


@app.task
def send_spam_email(user_email):
    send_mail(user_email)


@shared_task
def send_summary():
    receive()








from fastapi import Request, FastAPI

@app.post("/dummypath")
async def get_body(request: Request):
    return await request.body()