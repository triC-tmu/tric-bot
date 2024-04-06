from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import requests


def get_yukicoder_contests():
    """codeforcesの翌日開催のコンテスト情報を取得する"""
    url = "https://yukicoder.me/api/v1/contest/future"
    contests = requests.get(url).json()
    #[{"Id":490,"Name":"yukicoder contest (ゲーム問題コンテスト)","Date":"2024-04-12T21:20:00+09:00","EndDate":"2024-04-12T23:20:00+09:00","ProblemIdList":[10173,10164,10462,9080,9085,10191,10158]},{"Id":488,"Name":"yukicoder contest","Date":"2024-04-19T21:20:00+09:00","EndDate":"2024-04-19T23:20:00+09:00","ProblemIdList":[10755,10761,10756,10757,10758,10643,10762,10759]}]
    # コンテスト情報を格納するためのリスト
    contests_info = []

    # 現在の日付と時刻
    now = datetime.now()

    # 明日の日付
    tomorrow = now + timedelta(days=1)
    tomorrow_start = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    tomorrow_end = tomorrow_start + timedelta(days=1)


    for contest in contests:
        start_time = contest["Date"]
        contest_name = contest["Name"]
        url = f"https://yukicoder.me/contests/{contest['Id']}"
        dt = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z")
        if (
            int(tomorrow_start.timestamp()) 
            <= int(dt.timestamp()) 
            < int(tomorrow_end.timestamp())
        ):
            formatted_dt_jst = dt.strftime("%Y-%m-%d %H:%M:%S JST")
            contests_info.append((contest_name, formatted_dt_jst, url))

    return contests_info


if __name__ == "__main__":
    contests_info = get_yukicoder_contests()
    for name, start_time, url in contests_info:
        print(f"コンテスト名: {name}, 開催日時: {start_time}, {url}")
