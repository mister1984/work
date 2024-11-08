import asyncio
import datetime
import pandas as pd
import random as r
import re
from telethon import TelegramClient, functions, types, errors, utils
from telethon.tl.types import Channel, Chat, User, DocumentAttributeVideo
from pyrogram import Client, filters
n = int(input('Select number of bot >>> '))
df = pd.DataFrame()
df0 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='channels')
df1 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='credentials')
df4 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='our_channels')
client = TelegramClient(f'code/tg/telethon/{df1["app"][n]}', df1['id'][n], df1['hash'][n])
async def main():
    repeated, old_channles, files = [], [], []
    t = r.randint(10, 30)
    message = df1['text'][n]
    try: media_id = df1['media_id'][n].split('$')
    except AttributeError: media_id = []
    try:
        groups_id = df1['groups_id'][n].split('-')
        next_id, last_id = int(groups_id[0])-2, int(groups_id[1])-2
    except AttributeError:
        groups_id, min_id, max_id = -1, -1, -1
    me = await client.get_me()
    entry = int(input(f'Welcome, {me.first_name}\nHave {len(media_id)} attachments!\n1 >>> leave groups\n2 >>> suggest post\n3 >>> fresh groups\n>>> '))
    if entry == 1:
        our_channels = [int(j) for j in df4['id']]
        dialogs = await client.get_dialogs()
        for id, i in enumerate(dialogs):
            if i.entity.id not in our_channels: 
                await client.delete_dialog(dialogs[id])
                print(id)
    elif entry == 2:
        files = []
        for id, i in enumerate(media_id):
            file = await client.upload_file(i)
            files.append(i)
        for id, i in enumerate(df0['link']):
            if last_id >= id >= next_id:
                try:
                    try: bot = df0['bot'][id].split('$')
                    except (IndexError, AttributeError): bot = []
                    try: user = df0['user'][id].split('$')
                    except (IndexError, AttributeError): user = []
                    if len(bot) > 0:
                        for j in bot:
                            if j not in repeated:
                                peer = await client.get_input_entity(j)
                                peer_id, access_hash = peer.user_id, peer.access_hash
                                result = await client(functions.messages.StartBotRequest(bot=peer_id, peer=me.id, start_param='start'))
                                await asyncio.sleep(1)
                                last_message = (await client.get_messages(peer_id, 1))[0]
                                await asyncio.sleep(1)
                                if last_message.message == 'Выберите ваш язык:':
                                    await last_message.click(text='Русский')
                                    await asyncio.sleep(1)
                                if len(media_id) == 0: await client.send_message(peer_id, message)
                                elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                                repeated.append(j)
                                print(id+2)
                                await asyncio.sleep(t)
                    elif len(user) > 0:
                        for j in user:
                            if j not in repeated:
                                peer = await client.get_input_entity(j)
                                peer_id, access_hash = peer.user_id, peer.access_hash
                                if len(media_id) == 0: await client.send_message(peer_id, message)
                                elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                                repeated.append(j)
                                print(id+2)
                                await asyncio.sleep(t)
                except (TypeError, ValueError, AttributeError, errors.rpcerrorlist.PeerFloodError, errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.BotInvalidError) as e: 
                    if '(caused by StartBotRequest)' in str(e):
                        peer = await client.get_input_entity(j)
                        peer_id, access_hash = peer.user_id, peer.access_hash
                        if len(media_id) == 0: await client.send_message(peer_id, message)
                        elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                        print(id+2)
                        await asyncio.sleep(t)
                    else: print(i.strip(), e)
                except errors.FloodWaitError as e:
                    print('Flood wait for ', e.seconds)
                    if e.seconds > 7200: break
                    await asyncio.sleep(e.seconds)
                    try:
                        try: bot = df0['bot'][id].split('$')
                        except (IndexError, AttributeError): bot = []
                        try: user = df0['user'][id].split('$')
                        except (IndexError, AttributeError): user = []
                        if len(bot) > 0:
                            for j in bot:
                                if j not in repeated:
                                    peer = await client.get_input_entity(j)
                                    peer_id, access_hash = peer.user_id, peer.access_hash
                                    result = await client(functions.messages.StartBotRequest(bot=peer_id, peer=me.id, start_param='start'))
                                    await asyncio.sleep(1)
                                    last_message = (await client.get_messages(peer_id, 1))[0]
                                    await asyncio.sleep(1)
                                    if last_message.message == 'Выберите ваш язык:':
                                        await last_message.click(text='Русский')
                                        await asyncio.sleep(1)
                                    if len(media_id) == 0: await client.send_message(peer_id, message)
                                    elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                                    repeated.append(j)
                                    print(id+2)
                                    await asyncio.sleep(t)
                        elif len(user) > 0:
                            for j in user:
                                if j not in repeated:
                                    peer = await client.get_input_entity(j)
                                    peer_id, access_hash = peer.user_id, peer.access_hash
                                    if len(media_id) == 0: await client.send_message(peer_id, message)
                                    elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                                    repeated.append(j)
                                    print(id+2)
                                    await asyncio.sleep(t)
                    except (TypeError, ValueError, AttributeError, errors.rpcerrorlist.PeerFloodError, errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.BotInvalidError) as e: 
                        if '(caused by StartBotRequest)' in str(e):
                            peer = await client.get_input_entity(j)
                            peer_id, access_hash = peer.user_id, peer.access_hash
                            if len(media_id) == 0: await client.send_message(peer_id, message)
                            elif len(media_id) > 0: await client.send_file(peer_id, files, supports_streaming=True, caption=message)
                            print(id+2)
                            await asyncio.sleep(t)
                        else: print(i.strip(), e)
    elif entry == 3:
        current_time = str(datetime.datetime.now())[:10]
        min_time = int(re.sub('-', '', current_time)) - 10
        print(current_time)
        for id, i in enumerate(df0['id']):
            i = int(i)
            if last_id >= id >= next_id:
                try:
                    last_message = (await client.get_messages(int(str(i)[4:]), 1))[0]
                    post_time = str(last_message.date)[:10]
                    post_time = int(re.sub('-', '', date))
                    if post_time >= min_time: old_channles.append(1)
                    elif post_time < min_time: old_channels.append(0)
                    else: old_channels.append(-1)
                    print(id+2)
                except (TypeError, ValueError, AttributeError, errors.rpcerrorlist.PeerFloodError, errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.BotInvalidError) as e: print(df0['link'][id].strip(), e)
                except errors.FloodWaitError as e:
                    print('Flood wait for ', e.seconds)
                    if e.seconds > 7200: break
                    await asyncio.sleep(e.seconds)
                    try:
                        last_message = (await client.get_messages(int(str(i)[4:]), 1))[0]
                        date = str(last_message.date)[:10]
                        post_time = int(re.sub('-', '', date))
                        if post_time >= min_time: old_channles.append(1)
                        elif post_time < min_time: old_channels.append(0)
                        else: old_channels.append(-1)
                        print(id+2)
                    except (TypeError, ValueError, AttributeError, errors.rpcerrorlist.PeerFloodError, errors.rpcerrorlist.UsernameInvalidError, errors.rpcerrorlist.BotInvalidError) as e: print(df0['link'][id].strip(), e)
        df['status'] = old_channels
        df.to_excel(f'{next_id}-{last_id}.xlsx') 
with client:
    client.loop.run_until_complete(main())
