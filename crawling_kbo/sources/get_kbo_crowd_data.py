from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup


# ✅ 관중 수 테이블에서 어제 날짜 기준 데이터 가져오기
def get_kbo_crowd_data():
    url = "https://www.koreabaseball.com/Record/Crowd/GraphDaily.aspx"
    response = requests.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.table.find_all("tr")

    crowd_data = {}

    for row in rows[1:]:  # 첫 번째 행은 헤더
        cols = row.find_all("td")
        date = cols[0].text.strip()

        try:
            KST = timezone(timedelta(hours=9))
            yesterday_kst = datetime.now(KST).date() - timedelta(days=1)
            yesterday_str = yesterday_kst.strftime("%Y/%m/%d")
            if date == yesterday_str:
                # 예: '[두산-LG]' → 두산, LG
                home_team_name = cols[2].text.strip()
                out_team_name = cols[3].text.strip()
                # 예: '2,000' → 2000
                crowd_number = int(cols[5].text.strip().replace(',', ''))

                crowd_data[f"{out_team_name}"] = crowd_number
                crowd_data[f"{home_team_name}"] = crowd_number
                
        except Exception as e:
            print(f"날짜 파싱 오류: {e}")

    return crowd_data

if __name__ == "__main__":
    get_kbo_crowd_data()