import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def load_topics():
    df = pd.read_csv("db/localdata/topics.csv")
    return list(zip(df["topic_id"], df["text"]))


def load_opinions():
    path = os.path.join(BASE_DIR, "../../db/localdata/opinions.csv")
    return pd.read_csv(path)
