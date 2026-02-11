from telethon import TelegramClient, events
import os
import asyncio

api_id = int(os.environ.get("TG_API_ID", "123456"))
api_hash = os.environ.get("TG_API_HASH", "your_api_hash")
bot_token = os.environ.get("TG_BOT_TOKEN", "your_bot_token")

client = TelegramClient('bot_session', api_id, api_hash).start(bot_token=bot_token)

@client.on(events.NewMessage(pattern='/start'))
async def start(event):
    await event.respond("🤖 七号技师 Bot 已启动，发送 /send groupA 开始群发")

@client.on(events.NewMessage(pattern='/send (.+)'))
async def send_group(event):
    group = event.pattern_match.group(1)
    await event.respond(f"🚀 正在执行群发任务（分组：{group}）")
    # 这里可替换为调用 flask 后端接口
    os.system(f"curl http://localhost:5000/send_group?group={group}")

@client.on(events.NewMessage(pattern='/status'))
async def status(event):
    await event.respond("✅ 群发状态：全部发送成功")

print("🤖 Bot 正在运行中...")
client.run_until_disconnected()
