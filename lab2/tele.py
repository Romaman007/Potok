from pyrogram import Client
from pyrogram import types, filters
import asyncio
import pandas as pd
import datetime

CHANNEL_ID = [-1002029455841]
period = 10
app = Client(
    "ddd",
    api_id=
    api_hash=""
)


@app.on_message(filters=filters.channel)
def my_handler(client: Client, message: types.Message):
    if message.chat.id not in CHANNEL_ID:
        return
    media = 'Yes' if message.media!=None else 'None' 
    timestamp = message.date.strftime('%Y%m%d%H%M%S')
    to_pd.append([timestamp,message.chat.title,message.text,media])


async def main():
    global to_pd
    while True:
        to_pd =[]
        await asyncio.sleep(period)
        df = pd.DataFrame(to_pd, columns =['Date','name','text','media'])
        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        df.to_parquet(f'dfs/Data_for_{period}_sec_at{timestamp}.parquet', index=False)

app.start()
app.run(main())


