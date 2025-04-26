import os

import pandas as pd
import requests
from bs4 import BeautifulSoup
from loguru import logger

url = "https://news.naver.com/section/101"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.4 Safari/605.1.15"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 제목 strong 태그 추출
news_titles = soup.select(".sa_text .sa_text_strong")

logger.debug(f"발견한 뉴스 제목 수: {len(news_titles)}")

# 추출한 제목과 링크를 리스트로 저장
titles = []
links = []

for title_tag in news_titles:
    title = title_tag.get_text(strip=True)
    # 부모인 <a> 태그에서 href 가져오기
    parent_a_tag = title_tag.find_parent("a")
    if parent_a_tag:
        link = parent_a_tag.get("href")
    else:
        link = None  # 혹시나 a가 없는 경우 대비

    titles.append(title)
    links.append(link)

# 결과 출력
for i in range(min(5, len(titles))):  # 처음 5개만 출력
    logger.debug("뉴스 제목:", titles[i])
    logger.debug("뉴스 링크:", links[i])
    logger.debug("-" * 50)


# 새로운 데이터 (크롤링한 결과)
new_data = pd.DataFrame({"Title": titles, "Link": links})

# 기존 파일이 있으면 불러오기
if os.path.exists("news_titles.csv"):
    existing_data = pd.read_csv("news_titles.csv")
    # 기존 데이터에 새로운 데이터 추가
    combined_data = pd.concat([existing_data, new_data], ignore_index=True)
else:
    combined_data = new_data  # 처음이면 새로 시작

# 중복 제거 (옵션) - 제목+링크 둘 다 같으면 중복으로 보기
combined_data = combined_data.drop_duplicates(subset=["Title", "Link"])

# CSV 파일로 저장
combined_data.to_csv("news_titles.csv", index=False, encoding="utf-8-sig")

logger.success("CSV 파일 누적 저장 완료!")
