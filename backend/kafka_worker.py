import os
import json
import grpc
import logging
import analysis_pb2
import analysis_pb2_grpc
from confluent_kafka import Consumer, Producer
from google.protobuf.json_format import MessageToDict

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("worker_logger")

KAFKA_SERVER = os.getenv("KAFKA_SERVER", "kafka:9092")
CONSUME_TOPIC = "comments-input"
PRODUCE_TOPIC = "analysis-results"
CLIENT_GROUP = "ai-analysis-group"

kafka_consumer = Consumer(
    {
        "bootstrap.servers": KAFKA_SERVER,
        "group.id": CLIENT_GROUP,
        "auto.offset.reset": "earliest",
    }
)
kafka_producer = Producer({"bootstrap.servers": KAFKA_SERVER})

kafka_consumer.subscribe([CONSUME_TOPIC])


def call_grpc_analysis(comment_list):
    try:
        grpc_channel = grpc.insecure_channel("grpc-server:50051")
        grpc_stub = analysis_pb2_grpc.AnalysisServiceStub(grpc_channel)
        grpc_request = analysis_pb2.AnalyzeRequest(comments=comment_list)
        grpc_response = grpc_stub.Analyze(grpc_request)
        return MessageToDict(grpc_response)
    except Exception as exc:
        logger.error(f"gRPC call failed: {exc}")
        return None


logger.info("Kafka analysis worker is running...")

try:
    while True:
        kafka_msg = kafka_consumer.poll(1.0)
        if kafka_msg is None:
            continue
        if kafka_msg.error():
            logger.error(f"Consumer error: {kafka_msg.error()}")
            continue

        try:
            msg_data = json.loads(kafka_msg.value())
            task_id = msg_data.get("request_id")
            input_comments = msg_data.get("comments", [])
            logger.info(f"Received task_id={task_id} input_comments={input_comments}")

            analysis_result = call_grpc_analysis(input_comments)
            if analysis_result is None:
                logger.error(f"No analysis result for task_id={task_id}")
                continue

            outgoing_msg = {
                "request_id": task_id,
                "result": analysis_result,
            }
            kafka_producer.produce(
                PRODUCE_TOPIC, json.dumps(outgoing_msg).encode("utf-8")
            )
            kafka_producer.flush()
            logger.info(
                f"Processed & published result for task_id={task_id} to {PRODUCE_TOPIC}"
            )
        except Exception as err:
            logger.error(f"Kafka worker main loop exception: {err}")
except KeyboardInterrupt:
    logger.info("Worker exiting...")
finally:
    kafka_consumer.close()
