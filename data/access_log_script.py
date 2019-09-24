from kafka import KafkaConsumer
import json
import time


time.sleep(30)

consumer = KafkaConsumer('access-log-topic', group_id='access-indexer', bootstrap_servers=['kafka:9092'])


for message in consumer:
    f = open("access.log", "a")
    access = json.loads((message.value).decode('utf-8'))
    f.write(access['user_id'] + "\t" + access['item_id'] + "\n")
    f.close()
