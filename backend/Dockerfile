FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ARG TOPIC_MODEL=sentence-transformers/all-MiniLM-L6-v2
ARG CLASSIFIER_MODEL=facebook/bart-base
ARG SUMMARY_MODEL=google/flan-t5-base

ENV TOPIC_MODEL=${TOPIC_MODEL}
ENV CLASSIFIER_MODEL=${CLASSIFIER_MODEL}
ENV SUMMARY_MODEL=${SUMMARY_MODEL}
ENV HF_HOME=/app/.cache/huggingface

RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('${TOPIC_MODEL}')"
RUN python -c "from transformers import pipeline; pipeline('zero-shot-classification', model='${CLASSIFIER_MODEL}')"
RUN python -c "from transformers import pipeline; pipeline('summarization', model='${SUMMARY_MODEL}')"

ENV HOST=0.0.0.0
ENV PORT=8080

# COPY start.sh /start.sh
# RUN chmod +x /start.sh
# CMD ["/start.sh"]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
