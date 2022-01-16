import os

from celery.exceptions import MaxRetriesExceededError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery import Celery
from celery.utils.log import get_task_logger


# Create the celery app and get the logger
celery_app = Celery(broker=os.getenv('CELERY_BROKER_URL'))
logger = get_task_logger(__name__)


class Envs:
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_FROM = os.getenv('MAIL_FROM')
    MAIL_PORT = int(os.getenv('MAIL_PORT'))
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_FROM_NAME = os.getenv('MAIN_FROM_NAME')


@celery_app.task(name="send_mail", bind=True)
def send_mail(self, msg):
    login = Envs.MAIL_USERNAME
    password = Envs.MAIL_PASSWORD
    url = Envs.MAIL_SERVER
    email_msg = MIMEMultipart()
    email_msg['Subject'] = 'Trade is ready'
    email_msg['From'] = Envs.MAIL_FROM
    body = "Сделка состоялась. Поздравляем!"
    email_msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL(url, 465)
        server.login(login, password)
        server.sendmail(login, msg['email_address'], email_msg.as_string())
        logger.info("Email was send to address: %s" % (msg['email_address']))
        server.quit()
    except Exception as exc:
        logger.error("No connect to: %s, exception message: %s" % (url, str(exc)))
        try:
            self.retry(countdown=60*1)
        except MaxRetriesExceededError as err:
            logger.error("All retries are succeded: %s, exception message: %s" % (url, str(err)))
