import os

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import app_commands
from dotenv import load_dotenv

from atcoder import get_atcoder_contests, get_members_ac, get_problems_difficulty
from codeforces import get_codeforces_contests
from triC_member import add_member, get_members

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


async def send_message(message, channel_id=CHANNEL_ID):
    """指定したチャンネルIDにメッセージを送信する関数"""
    channel = client.get_channel(int(channel_id))
    if channel:
        await channel.send(message)
    else:
        print(f"Channel with ID {channel_id} not found.")


async def ac_alert():
    ac_submissions = get_members_ac()
    flat_list = [item for sublist in ac_submissions for item in sublist]
    ac_list = [submission["problem_id"] for submission in flat_list]
    ac_submissions_difficulty = get_problems_difficulty(ac_list)
    for submission in ac_submissions:
        msg = ""
        for s in submission:
            if s["result"] == "AC":
                difficulty = ac_submissions_difficulty[s["problem_id"]]
                if difficulty < 400:
                    color = ":hai:"
                elif difficulty < 800:
                    color = ":cha:"
                elif difficulty < 1200:
                    color = ":midori:"
                elif difficulty < 1600:
                    color = ":mizu:"
                elif difficulty < 2000:
                    color = ":ao:"
                elif difficulty < 2400:
                    color = ":ki:"
                elif difficulty < 2800:
                    color = ":daidai:"
                else:
                    color = ":aka:"
                msg += f"{s['user_id']}が{color}{s['problem_id']}をACしました。\n https://atcoder.jp/contests/{s['contest_id']}/submissions/{s['id']}\n"
        await send_message(msg)


async def atcoder_contest():
    contests_info = get_atcoder_contests()
    for name, start_time, url in contests_info:
        await send_message(
            f"{name}が開催されます \n 開催日時: {start_time}, https://atcoder.jp{url}"
        )
    return contests_info


async def codeforces_contest():
    contests_info = get_codeforces_contests()
    for name, start_time, url in contests_info:
        await send_message(f"{name}が開催されます \n 開催日時: {start_time}, {url}")
    return contests_info


async def yukicoder_contest():
    pass


async def contest_alert():
    # 毎日10時にcronで実行する
    await atcoder_contest()
    await codeforces_contest()


# スケジューラのインスタンスを作成
scheduler = AsyncIOScheduler()


@client.event
async def on_ready():
    print("起動")
    # スケジュールされたタスクを追加
    scheduler.add_job(contest_alert, "cron", hour=19, minute=0)
    scheduler.add_job(ac_alert, "interval", hours=2)

    # スケジューラを開始
    scheduler.start()
    await tree.sync()  # スラッシュコマンドを同期


@tree.command(name="ping", description="pingを返します。")
async def ping_command(interaction: discord.Interaction):
    await interaction.response.send_message("pong", ephemeral=False)


@tree.command(name="add_member", description="メンバーを追加します。")
async def add_member_command(interaction: discord.Interaction, user_id: str):
    add_member(user_id)
    await interaction.response.send_message(
        f"{user_id}を追加しました。", ephemeral=False
    )


@tree.command(name="get_members", description="メンバー一覧を取得します。")
async def get_members_command(interaction: discord.Interaction):
    members = get_members()
    await interaction.response.send_message(members, ephemeral=False)


client.run(DISCORD_TOKEN)
