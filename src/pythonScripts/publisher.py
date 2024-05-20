import asyncio
import pandas as pd
import nats
from nats.errors import TimeoutError
import json

async def main():
    nc = await nats.connect("172.19.0.1:4222")

    # Create JetStream context.
    js = nc.jetstream()
    parquet_file_path = '../EventSimulator/datasets/split.parquet'
    df = pd.read_parquet(parquet_file_path)

    await js.delete_stream(name="youtube-news")
    # Persist messages on 'foo's subject.
    await js.add_stream(name="youtube-news", subjects=["taxi-ride"])

    for i in range(len(df.index)):
        ack = await js.publish("taxi-ride", json.dumps({"ride_id": f"{df.iloc[i].iloc[0]}", "timestamp": f"{df.iloc[i].iloc[2]}", "pickup_longitude": float(df.iloc[i].iloc[3]), "pickup_latitude": float(df.iloc[i].iloc[4]), "dropoff_longitude": float(df.iloc[i].iloc[5]), "dropoff_latitude": float(df.iloc[i].iloc[6]), "passenger_count": int(df.iloc[i].iloc[7]), "fare_amount": float(df.iloc[i].iloc[1]) }).encode())
        print(ack)
        
    await nc.close()

if __name__ == '__main__':
    asyncio.run(main())