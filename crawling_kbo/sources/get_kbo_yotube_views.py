import os
import re
from datetime import datetime, timedelta, timezone

import requests
from loguru import logger

from dotenv import load_dotenv
# 로컬에서 환경변수 불러오기
load_dotenv()

# FIXME: github action 내에서 값이 제대로 안 가져와지는 부분 확인해야 함
# FIXME: 안 되면 그냥 클릭해서 가져오도록 만들기
# logger 설정
logger.add("logs/youtube_kbo.log", rotation="1 MB", level="DEBUG")
logger.add(lambda msg: print(msg, end=""), level="INFO")  # stdout에도 출력

# 환경변수에서 API Key 불러오기
API_KEY = os.environ.get("YOUTUBE_KEY")

# TVINGSPORTS 채널 ID
CHANNEL_ID = "UC8JtQf77wqhVpOQ8Cze8JjA"

# 어제 날짜 (KST 기준, 예: '4/12')
KST = timezone(timedelta(hours=9))
yesterday_kst = datetime.now(KST).date() - timedelta(days=1)
yesterday_str = f"{yesterday_kst.month}/{yesterday_kst.day}"
logger.info(f"✅ 기준 날짜: {yesterday_str}\n")


def get_kbo_yotube_views():
    video_ids = get_video_ids(CHANNEL_ID)
    filtered_videos = get_video_details(video_ids, yesterday_str)
    view_data = get_view_data(filtered_videos)

    logger.info(f"🎥 최종 View Data: {view_data}\n")
    return view_data


def get_video_ids(channel_id, max_results=30):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": API_KEY,
        "channelId": channel_id,
        "part": "snippet",
        "order": "date",            # 최신순 정렬
        "maxResults": max_results,
        "type": "video",
        "regionCode": "KR",
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])

    logger.debug(f"🔍 검색된 영상 수: {len(items)}")
    logger.debug(f"📋 Raw video list: {[item['snippet']['title'] for item in items]}")

    return [item["id"]["videoId"] for item in items]


def get_video_details(video_ids, date_keyword):
    details_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        "key": API_KEY,
        "part": "snippet,statistics",
        "id": ",".join(video_ids)
    }
    response = requests.get(details_url, params=params)
    response.raise_for_status()
    items = response.json().get("items", [])

    results = []
    for item in items:
        title = item["snippet"]["title"]
        views = int(item["statistics"].get("viewCount", 0))
        logger.debug(f"🎯 제목: {title}, 조회수: {views}")

        # 필터링 조건: 날짜 + 'KBO 리그' + '#shorts' 미포함
        if date_keyword in title and 'KBO 리그' in title:
            results.append({"title": title, "views": views})
    
    logger.info(f"📊 필터된 영상 수: {len(results)}")
    return results


def get_view_data(filtered_videos):
    view_data = {}
    for video in filtered_videos:
        title = video["title"]
        views = video["views"]

        match = re.search(r"\[(.*?) vs (.*?)\]", title)
        if match:
            team1, team2 = match.group(1), match.group(2)
            view_data[team1] = views
            view_data[team2] = views
            logger.debug(f"🏷️ {team1} vs {team2} → {views}회")

    return view_data


# 실행
if __name__ == "__main__":
    try:
        logger.info("🚀 유튜브 조회수 수집 시작")
        get_kbo_yotube_views()
    except Exception as e:
        logger.error(f"❌ 오류 발생: {e}")
