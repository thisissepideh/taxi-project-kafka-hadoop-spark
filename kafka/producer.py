import argparse, json, time
import pandas as pd
from kafka import KafkaProducer

ap = argparse.ArgumentParser()
ap.add_argument("--csv", required=True)
ap.add_argument("--n", type=int, default=9000)
ap.add_argument("--rate", type=float, default=100)     # پیام در ثانیه
ap.add_argument("--topic", default="taxi-trips")
a = ap.parse_args()

cols = ["pickup_datetime", "passenger_count", "trip_distance", "PULocationID",
        "DOLocationID", "fare_amount", "duration_min"]
df = pd.read_csv(a.csv, usecols=cols, nrows=300000)
df = df.sample(n=min(a.n, len(df)), random_state=42)

producer = KafkaProducer(bootstrap_servers="localhost:9092",
                         value_serializer=lambda v: json.dumps(v).encode("utf-8"))
for i, rec in enumerate(df.to_dict("records"), 1):
    producer.send(a.topic, rec)
    time.sleep(1.0 / a.rate)
    if i % 1000 == 0:
        print(f"sent {i}", flush=True)
producer.flush()
print("done", flush=True)
