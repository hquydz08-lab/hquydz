from telethon import TelegramClient
from telethon.sessions import StringSession
import asyncio

api_id = 34619338
api_hash = "0f9eb480f7207cf57060f2f35c0ba137"

async def main():
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        print(f"\n\nSESSION_START\n{client.session.save()}\nSESSION_END\n\n")

if __name__ == "__main__":
    asyncio.run(main())
