import msgpack as msgpack
from kafka import KafkaConsumer
from kafka import TopicPartition

def receive():
    consumer_conf = {'bootstrap.servers': 'localhost:9092',
                     'group.id': 'my_favorite_group',
                     'auto.offset.reset': "earliest"}

    consumer = KafkaConsumer(value_deserializer=consumer_conf)
    consumer.assign([TopicPartition('topic-email', 2)])
    msg = next(consumer)
    consumer.subscribe(['EMAIL_TOPIC'])
    for msg in consumer:
        assert isinstance(msg.value, dict)

# consumer = KafkaConsumer('topic-email')
#
# for msg in consumer:
#     print (msg)
#
# # join a consumer group for dynamic partition assignment and offset commits
# consumer = KafkaConsumer('topic-email', group_id='my_favorite_group')
# for msg in consumer:
#     print (msg)
#
# # manually assign the partition list for the consumer
# consumer = KafkaConsumer(bootstrap_servers='localhost:9092')
# consumer.assign([TopicPartition('topic-email', 2)])
# msg = next(consumer)
#
# # Deserialize msgpack-encoded values
# consumer = KafkaConsumer(value_deserializer=msgpack.loads)
# consumer.subscribe(['msgpackfoo'])
# for msg in consumer:
#     assert isinstance(msg.value, dict)
