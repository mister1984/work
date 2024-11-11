import requests, json
import asyncio
import datetime
import pandas as pd
import random as r
import re
import vk
import os
from telethon import TelegramClient, events, functions, types, errors
from telethon.tl.types import Channel, Chat, User
from telethon.tl.functions.channels import JoinChannelRequest
import logging
logging.basicConfig(level=logging.ERROR)
n = int(input('Select number of bot >>> '))
df = pd.DataFrame()
df1 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='credentials')
df2 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='credentials')
df3 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='content_channels')
df4 = pd.read_excel('code/vk/bots_vk.xlsx', sheet_name='content_groups')
client = TelegramClient(f'code/tg/telethon/{df1["app"][n]}', df1['id'][n], df1['hash'][n])
access_token=str(df2['token'][n][45:265])
api = vk.API(access_token=access_token, v='5.199')
channels=str(df3['id'][n]).split('$')
channels=[int(i) for i in channels]
vk_group_id=str(df4['id'][n]).split('$')
vk_group_id=[int(i) for i in vk_group_id]
messages_id = []
lock = asyncio.Lock()
@client.on(events.NewMessage(chats=channels))
async def my_event_handle(event):
    vk_media = []
    post = event.message
    async with lock:
        date0 = post.date.strftime('%s')
        if post.message and post.media and str(post.peer_id.channel_id)+'/'+str(post.id) not in messages_id:        
            text = post.message
            async for m in client.iter_messages(post.peer_id.channel_id, limit=10):
                date1 = m.date.strftime('%s')
                if (int(date0) - int(date1)) <= 60 and str(post.peer_id.channel_id)+'/'+str(m.id) not in messages_id:
                    media = await client.download_media(m)
                    media_type = re.search(r'[.]{1}[aA-zZ]+\d*', str(media)).group(0)
                    entry2 = media
                    if media_type.lower() in ['.jpeg', '.jpg', '.png', '.img']:
                        server = api.photos.getWallUploadServer(v='5.199')
                        url = server['upload_url']
                        photo = requests.post(url, files={'file1':open(entry2, 'rb')})
                        photo = photo.json()
                        photo = api.photos.save(album_id=server['album_id'], server=photo['server'], photos_list=photo['photo'], hash=str(photo['hash']))
                        photo_id = 'photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])
                        vk_media.append(photo_id)
                    elif media_type.lower() in ['.mp4', '.m4v', '.f4v', '.lrv']:
                        server = api.video.save(v='5.199')
                        url = server['upload_url']
                        video = requests.post(url, files={'file1':open(entry2, 'rb')})
                        video = video.json()
                        video_id = 'video'+str(video['owner_id'])+'_'+str(video['video_id'])
                        vk_media.append(video_id)
                    messages_id.append(str(post.peer_id.channel_id)+'/'+str(m.id))
                    os.remove(media)
            if vk_media and text: 
                for j in vk_group_id:
                    api.wall.post(owner_id=-j, from_group=1, message=text, attachments=vk_media, v='5.199')
            messages_id.append(str(post.peer_id.channel_id)+'/'+str(post.id))
            print(date0, 'Text and media')
        elif post.message and str(post.peer_id.channel_id)+'/'+str(post.id) not in messages_id:
            date1 = post.date.strftime('%s')
            text = post.message
            for j in vk_group_id:
                api.wall.post(owner_id=-j, from_group=1, message=text, v='5.199')
            messages_id.append(str(post.peer_id.channel_id)+'/'+str(post.id))
            print(date0,'Just text')
        elif post.media and str(post.peer_id.channel_id)+'/'+str(post.id) not in messages_id:
            text = []
            async for m in client.iter_messages(post.peer_id.channel_id, 10):
                date1 = m.date.strftime('%s')
                if (int(date0) - int(date1)) <= 120 and str(post.peer_id.channel_id)+'/'+str(m.id) not in messages_id:
                    if m.text: text.append(m.text)
                    media = await client.download_media(m)
                    media_type = re.search(r'[.]{1}[aA-zZ]+\d*', str(media)).group(0)
                    entry2 = media
                    if media_type.lower() in ['.jpeg', '.jpg', '.png', '.img']:
                        server = api.photos.getWallUploadServer(v='5.199')
                        url = server['upload_url']
                        photo = requests.post(url, files={'file1':open(entry2, 'rb')})
                        photo = photo.json()
                        photo = api.photos.save(album_id=server['album_id'], server=photo['server'], photos_list=photo['photo'], hash=str(photo['hash']))
                        photo_id = 'photo'+str(photo[0]['owner_id'])+'_'+str(photo[0]['id'])
                        vk_media.append(photo_id)
                    elif media_type.lower() in ['.mp4', '.m4v', '.f4v', '.lrv']:
                        server = api.video.save(v='5.199')
                        url = server['upload_url']
                        video = requests.post(url, files={'file1':open(entry2, 'rb')})
                        video = video.json()
                        video_id = 'video'+str(video['owner_id'])+'_'+str(video['video_id'])
                        vk_media.append(video_id)
                    messages_id.append(str(post.peer_id.channel_id)+'/'+str(m.id))
                    os.remove(media)
            if text and vk_media:     
                for j in vk_group_id:
                    api.wall.post(owner_id=-j, from_group=1, message=text[0], attachments=vk_media, v='5.199')
            elif not text and vk_media:
                for j in vk_group_id:
                    api.wall.post(owner_id=-j, from_group=1, attachments=vk_media, v='5.199')
            messages_id.append(str(post.peer_id.channel_id)+'/'+str(post.id))
            print(date0, 'Just media')
client.start()
client.run_until_disconnected()
