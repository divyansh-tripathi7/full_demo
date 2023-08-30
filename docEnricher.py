# from Helper_Functions import *
from kafka import KafkaProducer, KafkaConsumer
import json
from tqdm import tqdm
from Helper_Functions import *

print("start kr rha hu imports done")
# Initialize Kafka producer for DocEnrich
producer_enrich = KafkaProducer(bootstrap_servers='localhost:9092')
print("yaha hu ")
# Kafka consumer for DocExtractor topic
consumer_extractor = KafkaConsumer("DocExtractor", bootstrap_servers='localhost:9092')

print("consume krliya ")

for message in consumer_extractor:
    message_data = json.loads(message.value.decode('utf-8'))
    pdf_path = message_data["docPath"]
    doc_contents = get_pdf_text(pdf_path)
    
    print("topic content accessing")

    # Enrich the message with docContents and docSnippets
    enriched_text = preprocess_text(doc_contents)
    chunks = get_text_chunks(enriched_text)

    print("got text starting coreferencing")

    all_chunks = []

    for chunk in tqdm(chunks, desc = f"processing {pdf_path}"):
        chunk = coreferencing(chunk)
        all_chunks.append(chunk)

    print("cretaing enriched mssg")

    enriched_message = {
        "docID": message_data["docID"],
        "docPath": pdf_path,
        "docContents": doc_contents,
        "docSnippets": all_chunks  # Modify to suit your needs
    }

    print(enriched_message)

    # Publish enriched message to DocEnrich topic
    producer_enrich.send("DocEnrich", value=json.dumps(enriched_message).encode('utf-8'))


print("khaali hai topic")
producer_enrich.close()  # Close the producer when done