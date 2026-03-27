from fastapi import FastAPI
from kafka import KafkaProducer, KafkaConsumer
import json

app = FastAPI()

KAFKA_BOOTSTRAP_SERVERS = 'localhost:9092'

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

users_db = {
    1: {"id": 1, "name": "Alice"},
    2: {"id": 2, "name": "Bob"}
}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    user = users_db.get(user_id)
    if not user:
        return {"error": "User not found"}

    producer.send('user_requests', {'user_id': user_id})
    producer.flush()

    consumer = KafkaConsumer(
        'product_responses',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        consumer_timeout_ms=5000
    )

    for message in consumer:
        response = message.value
        if response.get('user_id') == user_id:
            consumer.close()
            return {**user, "products": response.get('products', [])}

    consumer.close()
    return {**user, "products": []}
