import os
import re
from datetime import datetime, timedelta, timezone

import requests

# 환경변수 불러오기
API_KEY = os.environ.get("YOUTUBE_KEY")

# TVINGSPORTS 채널 ID
CHANNEL_ID = "UC8JtQf77wqhVpOQ8Cze8JjA"

# 어제 날짜 (KST 기준, 예: '4/12')
KST = timezone(timedelta(hours=9))
yesterday_kst = datetime.now(KST).date() - timedelta(days=1)
yesterday_str = f"{yesterday_kst.month}/{yesterday_kst.day}"
    

def get_kbo_yotube_views():
    video_ids = get_video_ids(CHANNEL_ID)
    filtered_videos = get_video_details(video_ids, yesterday_str)
    view_data = get_view_data(filtered_videos)
    
    return view_data

# 영상 ID 수집
def get_video_ids(channel_id, max_results=20):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",
        "maxResults": max_results,
        "type": "video",
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])
    return [item["id"]["videoId"] for item in items]


# 영상 제목 + 조회수 수집
def get_video_details(video_ids, date_keyword):
    details_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {"key": API_KEY, "part": "snippet,statistics", "id": ",".join(video_ids)}
    response = requests.get(details_url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])

    results = []
    for item in items:
        title = item["snippet"]["title"]
        views = int(item["statistics"].get("viewCount", 0))
        
        # 🎯 날짜 포함 + 'KBO 리그' 포함하는 영상만
        if date_keyword in title and 'KBO 리그' in title:
            results.append({"title": title, "views": views})
    return results


def get_view_data(filtered_videos):
    view_data = {}
    for video in filtered_videos:
        title = video["title"]
        views = video["views"]

        match = re.search(r"\[(.*?) vs (.*?)\]", title)
        if match:
            team1, team2 = match.group(1), match.group(2)
            view_data[f"{team1}"] = views
            view_data[f"{team2}"] = views
            
    return view_data



# 실행
if __name__ == "__main__":
    try:
        video_ids = get_video_ids(CHANNEL_ID)
        filtered_videos = get_video_details(video_ids, yesterday_str)
        view_data = get_view_data(filtered_videos)
        print(view_data)
        
    except Exception as e:
        print("⚠️ 오류 발생:", e)
        
