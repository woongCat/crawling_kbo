import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timezone, timedelta
import os
import json

def append_to_google_sheets(crowd_data: dict, winrate_data: dict):
    # 날짜
    KST = timezone(timedelta(hours=9))
    today_str = datetime.now(KST).strftime('%-m/%-d')

    # 구글 시트 인증
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_JSON"))  # GitHub Secret에 등록된 JSON
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID"))

    for team in winrate_data.keys():
        try:
            worksheet = sheet.worksheet(team)
            crowd = crowd_data.get(team, '-')
            winrate = winrate_data.get(team, '-')

            row = [today_str, winrate, crowd, '', '']  # 날짜, 승률, 관중수, 영상 조회수, 좋아요 수
            worksheet.append_row(row)
            print(f"✅ {team} 저장 완료: {row}")
        except Exception as e:
            print(f"⚠️ {team} 저장 오류: {e}")
