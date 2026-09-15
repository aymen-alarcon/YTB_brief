import os
import requests as rqt
import pprint as pr 
from dotenv import load_dotenv


load_dotenv(".env")

base_url = os.getenv("URL")
api_key = os.getenv("API_KEY")

params = {
    "q": "@ElGrandeToto",
    "type": "channel",
    "key": api_key
}

response = rqt.get(f"{base_url}/search", params)
data = response.json()
channel_id = data["items"][0]["id"]["channelId"]

# print(channel_id)

params_2 = {
    "part": "contentDetails",
    "id": channel_id,
    "key": api_key
}

response_2 = rqt.get(f"{base_url}/channels", params_2)
data_2 = response_2.json()

playlist_id = data_2["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

# print(playlist_id)

params_3 = {
    "part": "contentDetails",
    "playlistId": playlist_id,
    "key": api_key,
    "maxResults": 25,
}

response_3 = rqt.get(f"{base_url}/playlistItems", params_3)
data_3 = response_3.json()

playlist_ids = []


for video in data_3["items"]:
    playlist_ids.append(video["contentDetails"]["videoId"])
    
# print(playlist_ids)

for id in playlist_ids:
    params_4 = {
        "part": "contentDetails",
        "id": id,
        "key": api_key,
    }

    response_4 = rqt.get(f"{base_url}/videos", params_4)
    data_4 = response_4.json()

    pr.pprint(data_4)