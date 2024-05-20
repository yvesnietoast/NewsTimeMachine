from googleapiclient.discovery import build
import re
from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi
import asyncio
import nats
from nats.errors import TimeoutError
import psycopg2
import model_pb2
def extract_video_id(url):
    # Regular expression to match YouTube video ID
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    
    # Find the video ID using the regular expression
    match = re.search(pattern, url)
    
    if match:
        return match.group(1)  # Return the video ID
    else:
        return None  # Return None if no match found

def get_video_info(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)

    # Get video details
    video_response = youtube.videos().list(
        part='snippet',
        id=video_id
    ).execute()
    # print(video_response)
    # Extract channel name and publication date
    channel_name = video_response['items'][0]['snippet']['channelTitle']
    publication_date = video_response['items'][0]['snippet']['publishedAt']
    title = video_response['items'][0]['snippet']['title']
    img = video_response['items'][0]['snippet']['thumbnails']['default']["url"]
    return channel_name, publication_date, title , img
def getTranscript(video_id):
    try:
        transcripts = YouTubeTranscriptApi.get_transcript(video_id)
        if transcripts:
            # Extract the transcripts as text
            subtitle_text = " ".join([entry["text"] for entry in transcripts])

            #print("Transcripts:")
            #print(subtitle_text)
        
            #print("Transcripts not available for this video.")
        return subtitle_text
    except Exception as e:
        #print("Not Available")
        return ("no transcript")


async def main():
    count=0
    api_key = 'AIzaSyDm4WlU3RE1Tnu92zM7DdyCE-qZX_r6GyU'
    
    
    #NATS/DATABASE CONNECTION
    nc = await nats.connect("172.19.0.6:4222")
    js = nc.jetstream()
    await js.delete_stream(name="youtube-news")
    await js.add_stream(name="youtube-news", subjects=["news"])
    
    

    file_path = "links.txt"
    #Puts each Newsbit in the jetstream. Creates protobuf
    with open(file_path, "r") as file:
        for line in file:
            text=line.strip() # Process each line here
            if(count%11==0 or text==''):
                category=text
                count+=1
                continue
            else:
                url = text
                video_id = extract_video_id(url)
                #print("category:",category)
               # print("YouTube Video ID:", video_id)

                channel_name, publication_date ,title , img= get_video_info(video_id, api_key)

               # print("Channel Name:", channel_name)
               # print("Publication Date:", publication_date)
                text = getTranscript(video_id)

                newsbit= model_pb2.newsBit()
                newsbit.title = title
                newsbit.channel = channel_name
                newsbit.transcript = text
                newsbit.category = category
                newsbit.publication_date = publication_date
                newsbit.video_url = url
                newsbit.image = img
                newsbit.guid = video_id
                count+=1
                ack = await js.publish("news",newsbit.SerializeToString())
                print(newsbit)
            print("\n\n")
    await nc.close()


    
if __name__ == "__main__":
    asyncio.run(main())