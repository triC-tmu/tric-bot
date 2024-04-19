import json
import math
from datetime import datetime, timedelta
from time import sleep

import requests
from bs4 import BeautifulSoup

from triC_member import get_members


def get_atcoder_contests():
    """AtCoderの翌日開催のコンテスト情報を取得する"""
    url = "https://atcoder.jp/contests/?lang=ja"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # コンテスト情報が含まれる要素を指定
    contests = soup.find_all("div", class_="table-responsive")

    # コンテスト情報を格納するためのリスト
    contests_info = []

    # 現在の日付と時刻
    now = datetime.now()

    # 明日の日付
    tomorrow = now + timedelta(days=1)
    tomorrow_start = datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    tomorrow_end = tomorrow_start + timedelta(days=1)

    for contest in contests:
        rows = contest.find("table").find_all("tr")[1:]  # ヘッダー行を除外
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 2:  # 必要な情報が含まれているか確認
                try:
                    contest_name = "".join(cols[1].text.strip().split()[2:])
                    start_time = cols[0].text.strip()
                    url = cols[1].find("a")["href"]
                except:
                    continue
                dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S%z").replace(
                    tzinfo=None
                )
                if tomorrow_start <= dt < tomorrow_end:
                    start_time = start_time.replace("+0900", " JST")
                    contests_info.append((contest_name, start_time, url))

    return contests_info


def get_ac_submissions(user, sleep_time=1):
    """2h前から現在までのAC提出を取得する"""
    now = int(datetime.now().timestamp())
    tow_hour_ago = now - 7200
    url = f"https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={user}&from_second={tow_hour_ago}"
    response = requests.get(url)
    sleep(sleep_time)
    return response.json()


def get_members_ac():
    members = get_members()
    ac_submissions = []
    for member in members:
        ac = get_ac_submissions(member)
        ac_submissions.append(ac)
    return ac_submissions


def get_problems_difficulty(problem_list: list) -> dict:
    """問題のdifficultyを取得する

    問題のdifficulty一覧を取得するAPIを叩いて特定の問題のdifficultyを返す

    Args:
        problem_list List[str]: difficultyを取得したい問題のidの配列
            problem_list = ["abc138_a", "abc_138_d"]

    Returns:
        Dict[str, int]: 問題名がkey, difficultyがvalueの連想配列 (difficultyが得られない場合はNone)
    """
    endpoint = "https://kenkoooo.com/atcoder/resources/problem-models.json"
    response = requests.get(endpoint)
    all_problems_model = json.loads(response.text)

    target_problems_difficulty = dict()

    try:
        for problem_name in problem_list:
            if problem_name in all_problems_model and "difficulty" in all_problems_model[problem_name]:
                diff = all_problems_model[problem_name]["difficulty"]
                if diff <= 400:
                    diff = round(400 / math.exp(1 - diff / 400))
            
                target_problems_difficulty[problem_name] = diff 

            else:
                target_problems_difficulty[problem_name] = None
                
        return target_problems_difficulty
    except KeyError:
        print(f"error: key was not found")
        return {}
    # https://github-wiki-see.page/m/sirogamichandayo/atcoder-diff-problems-go/wiki/diff%E3%81%AE%E3%83%9E%E3%82%A4%E3%83%8A%E3%82%B9%E3%82%92%E7%84%A1%E3%81%8F%E3%81%99%E8%A8%88%E7%AE%97%E5%BC%8F


if __name__ == "__main__":
    contests_info = get_atcoder_contests()
    for name, start_time, url in contests_info:
        print(f"コンテスト名: {name}, 開催日時: {start_time}, https://atcoder.jp{url}")

    ac_submissions = get_ac_submissions("Ayutaso")
    # {"id":9228183,"epoch_second":1577624760,"problem_id":"abc149_b","contest_id":"abc149","user_id":"Ayutaso","language":"Python3 (3.4.3)","point":0.0,"length":258,"result":"RE","execution_time":2104}
    for submission in ac_submissions:
        if submission["result"] != "AC":
            # https://atcoder.jp/contests/abc340/submissions/50170657
            print(
                f"{submission['user_id']}が{submission['problem_id']}をACしました。\n https://atcoder.jp/contests/{submission['contest_id']}/submissions/{submission['id']}"
            )
