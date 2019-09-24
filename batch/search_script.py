from elasticsearch import Elasticsearch
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json
from elasticsearch import Elasticsearch
import time

time.sleep(30)

consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])

es = Elasticsearch(['es'])

with open('db.json') as fixture:
	data = json.load(fixture)
while True:
	try:
		for element in data:
			if element['model'] == 'app.device':
				element['fields']['id'] = element['pk']
				es.index(index='listing_index', doc_type='listing', id=element['pk'], body=element['fields'])
		break
	except:
		continue

# es.index(index='listing_index', doc_type='listing', id=1, body={"owner": 1, "device_type": "drone", "manufacturer": "man", "device_model": "test", "price": 100.0, "rental_details": "weekly rental", "is_available": True, "updated_at": "2019-02-06T02:05:33.613Z", 'id': 1})
# es.index(index='listing_index', doc_type='listing', id=2, body={"owner": 2, "device_type": "VR headset", "manufacturer": "Oculus", "device_model": "Rift", "price": 100.0, "rental_details": "weekly rental", "is_available": True, "updated_at": "2019-02-06T02:05:33.613Z", 'id': 2})
es.indices.refresh(index="listing_index")

for message in consumer:
	some_new_listing = json.loads((message.value).decode('utf-8'))
	es.index(index='listing_index', doc_type='listing', id=some_new_listing['id'], body=some_new_listing)
	es.indices.refresh(index="listing_index")
	