from datetime import datetime, timezone, timedelta
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
import os

# ✅ 날짜 형식 완료
def append_to_google_sheets(crowd_data: dict, winrate_data: dict, view_data: dict):
    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST)
    
    # ✅ "4/26" 포맷으로 만듦
    today_str = today.strftime('%-m/%-d')  # Mac/Linux

    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    service_account_info = json.loads(os.getenv("SERVICE_ACCOUNT_JSON"))
    creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
    gc = gspread.authorize(creds)
    sheet = gc.open_by_key(os.getenv("GOOGLE_SHEET_ID"))

    for team in winrate_data.keys():
        try:
            worksheet = sheet.worksheet(team)
            crowd = crowd_data.get(team, '-')
            winrate = winrate_data.get(team, '-')
            view = view_data.get(team, '-')

            # ✅ "4/26"을 날짜로 인식하게 보내기
            row = [today_str, winrate, crowd, view, '']
            worksheet.append_row(row, value_input_option='USER_ENTERED')  # USER_ENTERED가 핵심
            print(f"✅ {team} 저장 완료: {row}")
        except Exception as e:
            print(f"⚠️ {team} 저장 오류: {e}")
