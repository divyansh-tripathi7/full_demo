from kafka import KafkaProducer, KafkaConsumer
import json
from Helper_Functions import *

# Kafka consumer for DocEnrich topic
consumer_enrich = KafkaConsumer("DocEnrich", bootstrap_servers='localhost:9092')

# Initialize Milvus collection here
vector_db = ...

for message in consumer_enrich:
    message_data = json.loads(message.value.decode('utf-8'))
    
    for snippet in message_data["docSnippets"]:
        # Ingest each snippet into Milvus collection
        processed_snippet = coreferencing(snippet)  # Apply coreference if needed
        vector_db.ingest([processed_snippet])
