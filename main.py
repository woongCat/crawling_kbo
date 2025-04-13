from sources.append_to_google_sheets import append_to_google_sheets
from sources.get_kbo_crowd_data import get_kbo_crowd_data
from sources.get_kbo_team_winrate_data import get_kbo_team_winrate_data
from sources.get_kbo_yotube_views import get_kbo_yotube_views

if __name__ == "__main__":
    try:
        # 1. 영상 조회수
        view_data = get_kbo_yotube_views()

        # 2. 관중 수
        crowd_data = get_kbo_crowd_data()

        # 3. 승률
        winrate_data = get_kbo_team_winrate_data()

        # 4. 스프레드시트에 저장
        append_to_google_sheets(crowd_data, winrate_data)

    except Exception as e:
        print("⚠️ 전체 실행 오류:", e)
