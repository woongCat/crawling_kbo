import requests
from bs4 import BeautifulSoup


def get_kbo_team_winrate_data():
    url = "https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx"
    response = requests.get(url)
    response.encoding = "utf-8"

    soup = BeautifulSoup(response.text, "html.parser")
    rows = soup.table.find_all("tr")

    team_data = {}

    for row in rows[1:]:  # 첫 번째 행은 헤더
        cols = row.find_all("td")
        if len(cols) >= 7:
            team_name = cols[1].text.strip()
            win_rate = cols[6].text.strip()
            team_data[team_name] = win_rate

    return team_data

if __name__ == "__main__":
    get_kbo_team_winrate_data()
