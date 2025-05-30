import json
import os
import uuid
from typing import List
from fastapi import APIRouter, Request
from pydantic import BaseModel
from confluent_kafka import Producer

router = APIRouter()


class AnalyzeRequest(BaseModel):
    comments: List[str]


class Opinion(BaseModel):
    type: str
    text: str


class TopicResult(BaseModel):
    topic_id: str
    topic_summary: str
    opinions: List[Opinion]
    conclusion: str


class AnalyzeResponse(BaseModel):
    topics: List[TopicResult]


KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
INPUT_TOPIC = "comments-input"
producer = Producer({"bootstrap.servers": KAFKA_BROKER})


@router.post("/analyze")
async def analyze_comments(request: Request):
    body = await request.json()
    comments = body.get("comments", [])
    request_id = str(uuid.uuid4())
    payload = {"request_id": request_id, "comments": comments}
    producer.produce(INPUT_TOPIC, json.dumps(payload).encode("utf-8"))
    producer.flush()
    return {"request_id": request_id}
