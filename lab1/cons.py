import pandas as pd
from confluent_kafka import Consumer, TopicPartition
import time

TOPIC_NAME = "some_topic"
PERIOD=20

consumer = Consumer({
    "bootstrap.servers": "localhost:9092",
    "group.id": "group1",
    "auto.offset.reset": "earliest"
})

tp = TopicPartition(topic=TOPIC_NAME, partition=0, offset=0)
consumer.assign([tp])
consumer.seek(tp)
while True:
    time.sleep(PERIOD)
    msg = consumer.consume(num_messages=1000, timeout=1.0)
    if len(msg) > 0:
        print((msg[0].value()).decode('utf-8')) 
    pand = []
    for i in range(len(msg)):
        pand.append(msg[i].value().decode('utf-8').split(' '))
    df = pd.DataFrame(pand, columns =['Date','Time','type','name','value'])
    df['value'] = df['value'].astype(int)
    print(df['value'].groupby(df['type']).mean())
    print(df['value'].groupby(df['name']).mean())

