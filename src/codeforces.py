import requests
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

def get_codeforces_contests():
    """codeforcesの翌日開催のコンテスト情報を取得する"""
    url = "https://codeforces.com/api/contest.list"
    # {"status":"OK","result":[{"id":1941,"name":"Codeforces Round (Div. 3)","type":"ICPC","phase":"BEFORE","frozen":false,"durationSeconds":8100,"startTimeSeconds":1710167700,"relativeTimeSeconds":-283770}
    contests = requests.get(url).json()["result"]

    # コンテスト情報を格納するためのリスト
    contests_info = []

    # 現在の日付と時刻
    now = datetime.now()

    # 明日の日付
    tomorrow = now + timedelta(days=1)
    tomorrow_start = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    tomorrow_end = tomorrow_start + timedelta(days=1)

    for contest in contests:
        start_time = contest["startTimeSeconds"]
        contest_name = contest["name"]
        url = f"https://codeforces.com/contest/{contest['id']}"
        if int(tomorrow_start.timestamp()) <= start_time < int(tomorrow_end.timestamp()):
            dt_utc = datetime.fromtimestamp(start_time, tz=timezone.utc)
            dt_jst = dt_utc.astimezone(ZoneInfo("Asia/Tokyo"))
            formatted_dt_jst = dt_jst.strftime('%Y-%m-%d %H:%M:%S JST')
            contests_info.append((contest_name, formatted_dt_jst, url))

    return contests_info

if __name__ == "__main__":
    contests_info = get_codeforces_contests()
    for name, start_time, url in contests_info:
        print(f"コンテスト名: {name}, 開催日時: {start_time}, {url}")