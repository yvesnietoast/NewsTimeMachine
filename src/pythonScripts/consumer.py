import asyncio
import nats
from nats.errors import TimeoutError
import model_pb2
import psycopg2


async def main():
    nc = await nats.connect("172.19.0.6:4222")
    #connecting to psql
    conn = psycopg2.connect(database="newstimemachine",
                           user="newstimemachine", 
                           password="password", 
                           host="172.19.0.5", 
                           port=5432)
    cur = conn.cursor()
    #cur.execute("INSERT INTO news_newsbit(title, channel, transcript,category,publication_date,video_url,image,guid) VALUES('testTitle','testChannel','TRANSCRIPT','CATEGORY','1999-01-08 04:05:06','testURL','testIMG','testGUID')")
    #cur.execute('SELECT * FROM news_newsbit;')
    #rows = cur.fetchall()
    conn.commit()
    #conn.close()
    


    # Create JetStream context.
    js = nc.jetstream()

    # Create ordered consumer with flow control and heartbeats
    # that auto resumes on failures.
    osub = await js.subscribe("news", ordered_consumer=True)
    data = bytearray()
    count=0
    while True:
        try:
            msg = await osub.next_msg()
            #print(msg.data)
            newsbit= model_pb2.newsBit()
            newsbit.ParseFromString(msg.data)
            print(newsbit.transcript)
            cur.execute(f"""INSERT INTO news_newsbit(title, channel, transcript, category, publication_date, video_url, image, guid) VALUES('{newsbit.title.replace("'","''")}', '{newsbit.channel}', '{newsbit.transcript.replace("'","''")}', '{newsbit.category}', '{newsbit.publication_date}', '{newsbit.video_url}', '{newsbit.image}', '{newsbit.guid}')""")

        

            print(newsbit.title.strip("\'"))
            conn.commit()
            #con.execute(f"INSERT INTO taxi VALUES ('{Data['ride_id']}', '{Data['timestamp']}', {Data['pickup_longitude']}, {Data['pickup_latitude']},  {Data['dropoff_longitude']}, {Data['dropoff_latitude']}, {Data['passenger_count']},{Data['fare_amount']})")
            count+=1
            print(count)
        except TimeoutError:
            break
    print("Consumer done")

    await nc.close()
    conn.close()

if __name__ == '__main__':
    asyncio.run(main())