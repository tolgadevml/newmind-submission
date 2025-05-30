import os
import json
import redis
from logger import logger
from confluent_kafka import Consumer

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
OUTPUT_TOPIC = "analysis-results"
GROUP_ID = "result-service-group"

results = {}

redis_host = os.getenv("REDIS_HOST", "redis")
r = redis.Redis(host=redis_host, port=6379, db=0)

consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
    }
)
consumer.subscribe([OUTPUT_TOPIC])

logger.info(f"Result Consumer listening on {OUTPUT_TOPIC}, broker={KAFKA_BROKER}")
try:
    while True:
        logger.debug("Polling for new Kafka messages...")
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            logger.error(f"Consumer error: {msg.error()}")
            continue

        try:
            data = json.loads(msg.value())
            request_id = data.get("request_id")
            result = data.get("result")
            if request_id:
                results[request_id] = result
                r.set(request_id, json.dumps(result), ex=3600)
                logger.info(f"Cached result for {request_id}")
            else:
                logger.warning("Message without request_id received!")
        except Exception as ex:
            logger.error(f"Failed to process message: {ex}")
except KeyboardInterrupt:
    logger.info("Result Consumer exiting...")
finally:
    consumer.close()
