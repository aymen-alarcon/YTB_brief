import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("URL")
API_KEY = os.getenv("API_KEY")


def get_channel_id(channel_name):
    params = {
        "q": channel_name,
        "type": "channel",
        "key": API_KEY
    }

    response = requests.get(f"{BASE_URL}/search", params=params)
    data = response.json()

    return data["items"][0]["id"]["channelId"]


def get_playlist_id(channel_id):
    params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": API_KEY
    }

    response = requests.get(f"{BASE_URL}/channels", params=params)
    data = response.json()

    return data["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]


def get_video_ids(playlist_id):
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "key": API_KEY,
        "maxResults": 25
    }

    response = requests.get(f"{BASE_URL}/playlistItems", params=params)
    data = response.json()

    return [
        video["contentDetails"]["videoId"]
        for video in data["items"]
    ]


def get_video_details(video_ids):
    videos = []

    for video_id in video_ids:
        params = {
            "part": "contentDetails,snippet,statistics",
            "id": video_id,
            "key": API_KEY
        }

        response = requests.get(f"{BASE_URL}/videos", params=params)
        data = response.json()

        videos.append(data["items"][0])

    return videos


def extract():
    channel_id = get_channel_id("@ElGrandeToto")
    playlist_id = get_playlist_id(channel_id)
    video_ids = get_video_ids(playlist_id)
    video_details = get_video_details(video_ids)

    return video_details
