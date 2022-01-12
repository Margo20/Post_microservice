import requests
from pykafka import KafkaClient

# client = KafkaClient(hosts="localhost:9092")

client = KafkaClient(hosts="10.1.0.111:9092")

consumer = client.topics["topic-email"].get_simple_consumer(
    consumer_group="mygroup",
    reset_offset_on_start=False)
for idx, message in enumerate(consumer):
    decoded_mail_address = message.value.decode()
    # send_mail(decoded_mail_address)
    requests.post(
        "http://fastapi:8080/my_send_email",
        json={
            "email_address": decoded_mail_address
        })
    # send_mail("rita.aniskovets@gmail.com")
    print(decoded_mail_address, idx)
    consumer.commit_offsets()
