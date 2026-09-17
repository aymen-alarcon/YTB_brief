import re
from datetime import datetime, timedelta

from datetime import timedelta

def parse_duration(duration):
    duration = duration[2:]

    hours = minutes = seconds = 0

    if "H" in duration:
        hours, duration = duration.split("H")
        hours = int(hours)

    if "M" in duration:
        minutes, duration = duration.split("M")
        minutes = int(minutes)

    if "S" in duration:
        seconds = int(duration[:-1])

    return timedelta(
        hours=hours,
        minutes=minutes,
        seconds=seconds
    ).total_seconds()

def transform(staging_data):
    for date in staging_data:
        raw_duration = parse_duration(date["contentDetails"]["duration"])

        raw_date = datetime.fromisoformat(date["snippet"]["publishedAt"].replace("Z", "+00:00"))

        date["snippet"]["publishedAt"] = raw_date
        date["contentDetails"]["duration"] = raw_duration
        date["statistics"]["viewCount"] = int(date["statistics"]["viewCount"])
        date["statistics"]["likeCount"] = int(date["statistics"]["likeCount"])
        date["statistics"]["favoriteCount"] = int(date["statistics"]["favoriteCount"])
        date["statistics"]["commentCount"] = int(date["statistics"]["commentCount"])

    print(staging_data)