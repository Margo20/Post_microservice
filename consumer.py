import os
import requests
from pykafka import KafkaClient
import logging.config
import yaml

with open('consumer_log.yaml', 'r') as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)
logging.config.dictConfig(config)
logger = logging.getLogger('consumer')

password = os.getenv('FASTAPI_PASSWORD')
client = KafkaClient(hosts="10.1.0.111:9092")

consumer = client.topics["topic-email"].get_simple_consumer(
    consumer_group="mygroup",
    reset_offset_on_start=False)
for idx, message in enumerate(consumer):
    logger.debug('received %s' % (message))
    decoded_mail_address = message.value.decode()
    logger.info('the consumer has successfully received: %s' % (decoded_mail_address))

    requests.post(
        "http://fastapi:8080/my_send_email",
        json={
            "email_address": decoded_mail_address,
            "password": password
        })
    # send_mail("rita.aniskovets@gmail.com")
    logger.info('email address: %s, index: %s' % (decoded_mail_address, idx))
    consumer.commit_offsets()
