import os
from logger import logger
from transformers import pipeline
from api.services.load_data import load_topics
from sentence_transformers import SentenceTransformer, util

TOPIC_MODEL = os.getenv("TOPIC_MODEL", "all-MiniLM-L6-v2")
CLASSIFIER_MODEL = os.getenv("CLASSIFIER_MODEL", "facebook/bart-base")
SUMMARY_MODEL = os.getenv("SUMMARY_MODEL", "google/flan-t5-base")

topic_model = SentenceTransformer(TOPIC_MODEL)
classifier = pipeline("zero-shot-classification", model=CLASSIFIER_MODEL)
summarizer = pipeline("summarization", model=SUMMARY_MODEL)
labels = ["claim", "counterclaim", "evidence", "rebuttal"]


def find_best_topic(comment, topic_sentences):
    logger.info("find_best_topic is running")
    comment_emb = topic_model.encode(comment, convert_to_tensor=True)
    topic_embs = topic_model.encode(topic_sentences, convert_to_tensor=True)
    sims = util.pytorch_cos_sim(comment_emb, topic_embs)[0]
    idx = sims.argmax().item()
    return idx, sims[idx].item()


def classify_opinion(comment):
    out = classifier(comment, labels)
    return out["labels"][0]


def generate_conclusion(topic, opinions):
    text = f"""Given the following topic and social media opinions, summarize the main perspective in a single, neutral conclusion.

    Topic: {topic}
    Opinions: {" ".join(opinions)}
    Conclusion:"""
    summary = summarizer(text, max_length=64, min_length=16, do_sample=False)
    return summary[0]["summary_text"]


def analyze_comments_pipeline(comments):
    logger.info("Analyze Comments Pipeline is running...")
    topics = load_topics()
    topic_texts = [t[1] for t in topics]

    topic_map = {i: (topics[i][0], topics[i][1]) for i in range(len(topics))}

    grouped = {i: [] for i in range(len(topics))}
    for comment in comments:
        idx, sim = find_best_topic(comment, topic_texts)
        label = classify_opinion(comment)
        grouped[idx].append({"text": comment, "type": label})

    results = []
    for idx, opinions in grouped.items():
        if not opinions:
            continue
        topic_id, topic_summary = topic_map[idx]
        conclusion = generate_conclusion(topic_summary, [o["text"] for o in opinions])
        results.append(
            {
                "topic_id": topic_id,
                "topic": topic_summary,
                "opinions": opinions,
                "conclusion": conclusion,
            }
        )
    logger.info("Analyze Comments Pipeline is completed successfully.")
    return results
