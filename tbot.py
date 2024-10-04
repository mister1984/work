import asyncio
import datetime
import pandas as pd
import random as r
import re
from telethon import TelegramClient, functions, types, errors
from telethon.tl.types import Channel, Chat, User
n = int(input('Select number of bot >>> '))
df = pd.DataFrame()
df0 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='channels')
df1 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='credentials')
df2 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='join')
df3 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='search')
df4 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='our_channels')
df5 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='users')

app = TelegramClient(f'code/tg/telethon/{df1["app"][n]}', df1['id'][n], df1['hash'][n])
async def main():        
    t = r.randint(10, 30)
    try:
        groups_id = df1['groups_id'][n].split('-')
        min_id, max_id = int(groups_id[0]), int(groups_id[1])
    except AttributeError:
        groups_id, min_id, max_id = -1, -1, -1
    ids, links, titles, members, types, topics, dates, descriptions, cities, regions, sub_regions, repeated, bots, users, suggests, topics, topics_checked, notes  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    me = await app.get_me()
    entry = int(input(f'Welcome, {me.first_name}\n1 >>> groups\n2 >>> posts\n>>> '))
    if entry == 1:
        entry = int(input('2 >>> leave\n>>> '))
        if entry == 2:
            our_channels = [int(j) for j in df4['id']]
            dialogs = await app.get_dialogs()
            for id, i in enumerate(dialogs):
                if i.entity.id not in our_channels: 
                    await app.delete_dialog(dialogs[id])
                    print(id)
    elif entry == 2:
        entry= int(input('4 >>> Suggest post\n>>> '))
        message = df1['text'][n]
        try: media_id = df1['media_id'][n].split('$')
        except AttributeError: media_id = []
        message_type = int(input('1 >>> Plain text\n2 >>> With media\n>>> '))
        for id, i in enumerate(df0['id']):
            if (max_id-2) >= id >= (min_id-2):
                try:
                    if entry == 4:
                        try: bot = df0['bot'][id].split('$')
                        except (IndexError, AttributeError): bot = []
                        try: user = df0['user'][id].split('$')
                        except (IndexError, AttributeError): user = [] 
                        if len(bot) > 0:
                            for j in bot:
                                if j not in repeated:
                                    peer = await app.get_input_entity(j)
                                    peer_id, access_hash = peer.user_id, peer.access_hash
                                    result = await app(functions.messages.StartBotRequest(bot=peer_id, peer=my.id, start_param='start'))
                                    await asyncio.sleep(1)
                                    last_message = (await app.get_messages(peer_id, 1))[0]
                                    await asyncio.sleep(1)
                                    if last_message.message == 'Выберите ваш язык:':
                                        await last_message.click(text='Русский')
                                        await asyncio.sleep(1)
                                    if message_type == 1: await app.send_message(peer_id, message)
                                    elif message_type == 2: await app.send_file(peer_id, media_id, caption=message) 
                                    repeated.append(j)
                                    print(id+2)
                                    await asyncio.sleep(t)
                        elif len(user) > 0:
                            for j in user:
                                if j not in repeated:
                                    peer = await app.get_input_entity(j)
                                    peer_id, access_hash = peer.user_id, peer.access_hash
                                    if message_type == 1: await app.send_message(peer_id, message)
                                    elif message_type == 2: await app.send_file(peer_id, media_id, caption=message) 
                                    repeated.append(j)
                                    print(id+2)
                                    await asyncio.sleep(t)
                except (TypeError, ValueError, AttributeError)  as e: print(e)
                except errors.rpcerrorlist.PeerFloodError as e: print(e)
                except errors.FloodWaitError as e:
                    print('Flood wait for ', e.seconds)
                    if e.seconds > 7200: break
                    await asyncio.sleep(e.seconds)                      
with app:
    app.loop.run_until_complete(main())
