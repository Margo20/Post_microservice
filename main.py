from project import create_app
from project.celery_utils import create_celery

app = create_app()
app.celery_app = create_celery()
celery = app.celery_app

@celery.task
def divide(x, y):
    import time
    time.sleep(5)
    return x / y

'''АБЫЧтошка'''
from fastapi import BackgroundTasks


def send_email(email, message):
    pass


@app.get("/")
async def ping(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "email@address.com", "Hi!")
    return {"message": "pong!"}



'''send_email'''
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_mail():
    login = "vania.vanin2021@gmail.com"
    password = "admin777admin"
    url = "smtp.gmail.com"
    toaddr = "vania.vanin2021@gmail.com"

    msg = MIMEMultipart()
    msg['Subject'] = 'Zagolovok'
    msg['From'] = "vania.vanin2021@gmail.com"
    body = "Получай!! Радуйся"
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(url, 465)
        server.login(login, password)
    except TimeoutError:
        print("No connect")

    server.login(login, password)
    server.sendmail(login, toaddr, msg.as_string())
    server.quit()

def main():
    send_mail()

if __name__ == "__main__":
    main()


