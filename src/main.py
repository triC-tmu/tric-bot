import os
import time

import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord import app_commands
from dotenv import load_dotenv

from atcoder import get_atcoder_contests, get_members_ac, get_problems_difficulty
from codeforces import get_codeforces_contests
from yukicoder import get_yukicoder_contests
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
    print(channel)
    if channel:
        if message:
            await channel.send(message)
        else:
            print("empyt message")
    else:
        print(f"Channel with ID {channel_id} not found.")

async def send_embedded_message(title, url, description, color=0xffffff,channel_id=CHANNEL_ID):
    """指定したチャンネルIDに埋め込みメッセージをembeddedで送信する関数"""
    channel = client.get_channel(int(channel_id))
    if channel:
        if url == "":
            embed = discord.Embed(title=title, description=description, color=color)
        else:
            embed = discord.Embed(title=title, url=url, description=description, color=color)
        await channel.send(embed=embed)
    else:
        print(f"Channel with ID {channel_id} not found.")


async def ac_alert():
    ac_submissions = get_members_ac()
    flat_list = [item for sublist in ac_submissions for item in sublist]
    ac_list = [submission["problem_id"] for submission in flat_list]
    ac_submissions_difficulty = get_problems_difficulty(ac_list)
    time.sleep(1)
    for submission in ac_submissions:
        msg = ""
        for s in submission:
            if s["result"] == "AC":
                if s["problem_id"] in ac_submissions_difficulty:
                    difficulty = ac_submissions_difficulty[s["problem_id"]]
                    if difficulty < 400:
                        color = "<:hai:1225032949964083251>"
                    elif difficulty < 800:
                        color = "<:cha:1225032948290687046>"
                    elif difficulty < 1200:
                        color = "<:midori:1225032946184880179>"
                    elif difficulty < 1600:
                        color = "<:mizu:1225032939683844108>"
                    elif difficulty < 2000:
                        color = "<:ao:1225032938157248563>"
                    elif difficulty < 2400:
                        color = "<:ki:1225032936634585128>"
                    elif difficulty < 2800:
                        color = "<:daidai:1225032935111921744>"
                    else:
                        color = "<:aka:1225032933606424576>"
                else:
                    color = ""
                msg += f"{s['problem_id']}{color} https://atcoder.jp/contests/{s['contest_id']}/submissions/{s['id']}\n"
        if msg:
            await send_embedded_message(
                title=f"{s['user_id']}が{len(submission)}問<:accepted:1110414595316781147>しました",
                description=msg,
                color=0x5cb85c
                )


async def atcoder_contest():
    contests_info = get_atcoder_contests()
    for name, start_time, url in contests_info:
        await send_embedded_message(
            title=f"{name}が開催されます",
            url=f"https://atcoder.jp{url}",
            description=f"開催日時: {start_time}",
            color=0xffffff
        )
    return contests_info


async def codeforces_contest():
    contests_info = get_codeforces_contests()
    for name, start_time, url in contests_info:
        await send_embedded_message(
            title=f"{name}が開催されます",
            url=f"{url}",
            description=f"開催日時: {start_time}",
            color=0x3b5998
            )
    return contests_info


async def yukicoder_contest():
    contests_info = get_yukicoder_contests()
    for name, start_time, url in contests_info:
        await send_embedded_message(
            title=f"{name}が開催されます",
            url=f"{url}",
            description=f"開催日時: {start_time}",
            color=0xc5dbee
            )
    return contests_info


async def contest_alert():
    # 毎日10時にcronで実行する
    await atcoder_contest()
    await codeforces_contest()
    await yukicoder_contest() 


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
