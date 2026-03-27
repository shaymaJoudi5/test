from kafka import KafkaConsumer, KafkaProducer
import json

KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

products_db = {
    1: [{"id": 1, "name": "Book"}, {"id": 2, "name": "Pen"}],
    2: [{"id": 3, "name": "Laptop"}]
}

def process_requests():
    consumer = KafkaConsumer(
        "user_requests",
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="products-group"
    )
    print("Products Service ecoute Kafka...")
    for message in consumer:
        user_id = message.value.get("user_id")
        products = products_db.get(user_id, [])
        producer.send("product_responses", {"user_id": user_id, "products": products})
        producer.flush()
        print("Reponse envoyee pour user_id=" + str(user_id))

if __name__ == "__main__":
    process_requests()
