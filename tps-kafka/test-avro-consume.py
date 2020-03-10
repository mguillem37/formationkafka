from confluent_kafka import KafkaError
from confluent_kafka.avro import AvroConsumer
from confluent_kafka.avro.serializer import SerializerError

broker = "localhost:9093"
topic =  'vehicle-positions-avro'
registry_url = 'http://localhost:8081'

c = AvroConsumer({
    'bootstrap.servers': broker,
    'group.id': 'vp-avro-consumer',
    'schema.registry.url': registry_url})

c.subscribe([topic])

while True:
    try:
        msg = c.poll(10)

    except SerializerError as e:
        print("Message deserialization failed for {}: {}".format(msg, e))
        break

    if msg is None:
        continue

    if msg.error():
        print("AvroConsumer error: {}".format(msg.error()))
        continue

    print(msg.value())

c.close()