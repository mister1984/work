import asyncio
from pyrogram.types import InputMediaPhoto, InputMediaVideo
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerSelf, InputUser, InputReportReasonSpam, InputPeerUser, InputGeoPoint, ReactionEmoji, InputPeerChannel
from pyrogram import Client, enums 
from pyrogram.errors import *
import datetime
import pandas as pd
import random as r
import re
async def main():        
    t = r.randint(5, 30)
    n = int(input('Select number of bot >>> '))
    df = pd.DataFrame()
    df0 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='channels')
    df1 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='credentials')
    df2 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='join')
    df3 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='search')
    df5 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='users')
    ids, links, titles, members, types, topics, dates, descriptions, cities, regions, sub_regions, repeated, bots, users, suggests, topics, topics_checked, notes  = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    def adding():
        if chat.id < 0:
            if int(chat.members_count) > 1000 and chat.id not in [j for j in df0['id']]:
                ids.append(chat.id)
                titles.append(chat.title)
                members.append(chat.members_count)
                descriptions.append(chat.description)
                try: links.append('https://t.me/'+chat.username)
                except: links.append('unknown')
                types.append(str(chat.type)[9:])
            elif chat.id in [j for j in df0['id']]: print('Chat', chat.title, 'in your base.')
            else: print('Chat has', chat.members_count, 'users.')
    def xlsx(mode):
        if mode == 'channels':
            df['id'] = ids
            df['link'] = links
            df['title'] = titles
            df['members'] = members
            df['type'] = types
            df['description'] = descriptions
            df.to_excel('channels.xlsx')
    try:
        groups_id = df1['groups_id'][n].split('-')
        min_id, max_id = int(groups_id[0]), int(groups_id[1])
    except AttributeError: 
        groups_id, min_id, max_id = -1, -1, -1 
    async with Client(df1['app'][n], df1['id'][n], df1['hash'][n]) as app: 
        me = await app.get_me()
        my_first_name = me.first_name
        my_id = me.id
        entry = int(input(f'Welcome, {my_first_name}\n1 >>> groups\n2 >>> posts\n3 >>> users\n4 >>> settings\n>>> '))
        if entry == 1:
            entry = int(input('0 >>> to_excel\n1 >>> join\n3 >>> search\n>>> '))
            if entry == 0:
                entry = int(input('1 >>> Get new\n2 >>> Get from dialogs\n>>> '))
                if entry == 1:
                    base_usernames = [i[13:] for i in df2['link']]
                    my_base_usernames = [i[13:] for i in df0['link']]
                    for id, k in enumerate(base_usernames):
                        if max_id >= id >= min_id and k not in my_base_usernames:
                            try:
                                chat = await app.get_chat(k)
                                await asyncio.sleep(0.25)
                                adding('new_chats')
                            except (AttributeError, TypeError) as e: print('Check it >>> https://t.me/'+chat.username)
                            except FloodWait as e:
                                print('Wait for', e.value, 'sec...')
                                if e.value > 3600: break
                                await asyncio.sleep(e.value)
                            except (BadRequest, NotAcceptable, UserDeactivated) as e: print(e.MESSAGE)
                elif entry == 2: 
                    id = -1
                    async for d in app.get_dialogs():
                        try:
                            id += 1
                            chat = d.chat
                            chat = await app.get_chat(chat.id)
                            await asyncio.sleep(0.25)
                            adding()
                        except (AttributeError, TypeError) as e: print('Errors')
                        except FloodWait as e:
                            print('Wait for', e.value, 'sec...')
                            if e.value > 3600: break
                            await asyncio.sleep(e.value)
                        except (BadRequest, NotAcceptable, UserDeactivated) as e: print(e.MESSAGE)
                xlsx('channels')    
            elif entry == 1:
                my_diologs_id = [d.chat.id async for d in app.get_dialogs()]
                for id, i in enumerate(df0['id']):
                    if (max_id-2) >= id >= (min_id-2) and i not in my_diologs_id:
                        try:
                            await app.join_chat(i)
                            print(id+2)
                            await asyncio.sleep(3)
                        except BadRequest:
                            try:
                                peer = await app.resolve_peer(df0['link'][id][13:])
                                await asyncio.sleep(0.25)
                                await app.join_chat(i)
                                await asyncio.sleep(3)
                                print(id+2)
                            except FloodWait as e:
                                print('Wait for', e.value, 'sec...')
                                if e.value > 3600: break
                                await asyncio.sleep(e.value)
                            except (BadRequest, NotAcceptable, UserDeactivated) as e: print(e.MESSAGE)
                        except FloodWait as e:
                            print('Wait for', e.value, 'sec...')
                            if e.value > 3600: break
                            await asyncio.sleep(e.value)
                        except (NotAcceptable, UserDeactivated) as e: print(e.MESSAGE)
            elif entry == 3:
                for id, i in enumerate(df3['word']):
                    try:
                        chat = await app.search_contacts(i)
                        for j in chat.global_results:
                            try: links.append('https://t.me/'+j.username)
                            except TypeError: links.append('-')
                            titles.append(j.title)
                            types.apped(j.type)
                        print(id) 
                        await asyncio.sleep(0.1)
                    except TypeError: print('Not find >>>' , i)
                    except FloodWait as e:
                        print('Wait for', e.value, 'sec...')
                        if e.value > 3600: break
                        await asyncio.sleep(e.value)
                df['link'] = links
                df['title'] = titles
                df['type'] = types
                df.to_excel(f'{df1["who"]}-search_results.xlsx')
        elif entry == 2: 
            entry= int(input('1 >>> Send to chats\n2 >>> Send to user\n3 >>> Comment on post\n>>> '))
            message = df1['text'][n]
            try: media_id = df1['media_id'][n].split('$')
            except AttributeError: media_id = []
            message_type = int(input('1 >>> Plain text\n2 >>> With media\n>>> '))
            for id, i in enumerate(df0['id']):
                if (max_id-2) >= id >= (min_id-2):
                    try:
                        if entry == 1 or entry == 2:
                            if message_type == 1: await app.send_message(i, message)
                            elif message_type == 2: await app.send_media_group(i, [InputMediaPhoto(media_id[0], caption=message)])  
                            async for m in app.get_chat_history(i):
                                print(r'https://t.me/'+ df0['username'][id] + r'/'+ str(m.id))
                                await asyncio.sleep(t)
                                break 
                        elif entry == 3:
                            comment = df1['text'][n].split('$')
                            c = r.randint(0, len(comment)-1)
                            try:
                                async for m in app.get_chat_history(i):
                                    m1 = await app.get_discussion_message(i, m.id) 
                                    if message_type == 1: await m1.reply(comment[c])
                                    elif message_type == 2: await m1.reply_media_group([InputMediaPhoto(media_id[0], caption=message)])
                                    async for m2 in app.get_discussion_replies(i, m.id):
                                        print(df0['link'] + r'/' + str(m.id) + r'?comment=' + str(m2.id))
                                        break
                                    break
                                await asyncio.sleep(t)
                            except (NotAcceptable, BadRequest, UserDeactivated) as e: print(e.MESSAGE)
                            except FloodWait as e:
                                print('wait for', e.value, 'sec...')
                                await asyncio.sleep(e.value)
                            except Forbidden:
                                try:
                                    await app.join_chat((await app.get_chat(i)).linked_chat.id) 
                                    m1 = await app.get_discussion_message(i, m.id)  
                                    if message_type == 1: await m1.reply(comment[c])
                                    elif message_type == 2: await m1.reply_media_group([InputMediaPhoto(media_id[0], caption=message)])
                                    async for m2 in app.get_discussion_replies(i, m.id):
                                        print(df0['link'][id] + r'/' + str(m.id) + r'?comment=' + str(m2.id))
                                        break
                                    await asyncio.sleep(t)
                                except FloodWait as e:
                                    print('wait for', e.value, 'sec...')
                                    await asyncio.sleep(e.value)
                                except (NotAcceptable, BadRequest, UserDeactivated) as e: print(e.MESSAGE)
                    except (NotAcceptable, BadRequest, UserDeactivated, Forbidden) as e: print(e.MESSAGE, df0['link'][id])
                    except FloodWait as e: 
                        print('Wait for', e.value, 'sec...')
                        if e.value > 3600: break
                        await asyncio.sleep(e.value) 
        elif entry == 3:
            entry = int(input('1 >>> Check status bot\n2 >>> Join\n3 >>> Repost\n4 >>> Likes\n5 >>> Search posts\n6 >>> YouScan parsing\n7 >>> Report peer\n>>> '))
            range_bots = input('Range bots >>> ').split('-')
            bot_next = int(range_bots[0])
            bot_last = int(range_bots[1])
            if entry == 7:
                user = input('User for report >>> ')
            elif entry == 2:
                link = input('Link on channel >>> ').split('https://t.me/')
                chat = link[1]
            elif entry == 5:
                m0 = int(input('Min date (yyyymmdd) >>> '))
            elif entry == 4 or entry == 7:
                link = input('Link on post >>> ').split('https://t.me/')
                link = link[1].split('/')
                chat = link[0]
                message_id = int(link[1])
                emoji = input('Emoji >>> ')
            for id, i in enumerate(df1['app']):
                if bot_last >= id >= bot_next:
                    print(id)
                    try:
                        async with Client(i, df1['id'][n], df1['hash'][n]) as app:
                            if entry == 1: await app.get_me()
                            elif entry == 2: await app.join_chat(chat)
                            elif entry == 7:
                                message = await app.get_messages(chat, message_id)
                                peer = await app.resolve_peer(user)
                                peer_id, access_hash = peer.user_id, peer.access_hash
                                await app.invoke(functions.account.ReportPeer(peer=InputPeerUser(user_id=peer_id, access_hash=access_hash), reason=InputReportReasonSpam(), message=message.caption)) 
                            elif entry == 4:
                                peer = await app.resolve_peer(chat)
                                peer_id = peer.channel_id
                                access_hash = peer.access_hash
                                await app.invoke(functions.messages.SendReaction(peer=InputPeerChannel(channel_id=peer_id, access_hash=access_hash), msg_id=message_id, reaction=[ReactionEmoji(emoticon=emoji)]))
                            elif entry == 5:
                                for q in df3['word'][0].split('$'):
                                    async for message in app.search_global(q):
                                        try:
                                            m1 = int(str(message.date)[:10])
                                        except (ValueError, AttributeError):
                                            m1 = m0
                                        if m1 >= m0:
                                            if message.text:
                                                i0 = message.text
                                                i = message.text.lower()
                                            elif message.caption:
                                                i0 = message.caption
                                                i = message.caption.lower()                                             
                                            i = re.sub('[,]', ' ', i)
                                            i = re.sub('[.]', ' ', i)
                                            i = re.sub('[(]', ' ', i)
                                            i = re.sub('[)]', ' ', i)
                                            i = re.sub('["]', ' ', i)
                                            i = re.sub("[']", ' ', i)
                                            i = re.sub("[|]", ' ', i)
                                            i = re.sub("[!]", ' ', i)
                                            i = re.sub("[?]", ' ', i)
                                            i = re.sub("[/]", ' ', i)
                                            i = re.sub('\n', ' ', i)
                                            i = re.sub(' +', ' ', i)
                                            if ' '+q.lower()+' ' in ' '+i.lower().strip()+' ': 
                                                dates.append(message.date)
                                                try:
                                                    link = r'https://t.me/'+message.chat.username+r'/'+str(message.id)
                                                except TypeError: 
                                                    link = r'https://t.me/'+message.chat.username
                                                links.append(link)
                                            titles.append(message.chat.title)
                                            descriptions.append(i0)
                    except (PeerIdInvalid, Unauthorized) as e: print(id, e.MESSAGE)
            if entry == 5:
                df['date'] = dates
                df['link'] = links
                df['title'] = titles
                df['description'] = descriptions
                df.to_excel('posts/'+q[0]+'.xlsx')  
            elif entry == 6:
                usernames, posts = [], []
                for id, i in enumerate(df2['link']):
                    i = i[13:]
                    i = i.split(r'/')
                    name = i[0]
                    if name not in [j[13:] for j in df0['link']]:
                        try: post_id = i[1]
                        except IndexError: post_id = '-'
                        if name not in usernames:
                            if re.search(r'bot$', name.lower().strip()) and len(i) == 1:
                                usernames.append('-bot')
                                posts.append('-')
                            elif name == 'c':
                                usernames.append('-undefined_groups  '+str(i[2]))
                                try:posts.append(i[3])
                                except IndexError: posts.append('-')
                            elif len(i) == 1:
                                usernames.append('-closed_groups  '+str(i[0]))
                                posts.append('-')
                            else:
                                usernames.append(name)
                                posts.append(post_id)
                        else:
                            usernames.append('-')
                            posts.append(post_id)
                df['username'] = usernames
                df['post_id'] = posts 
                df.to_excel('youscan.xlsx')
        elif entry == 4:  
            entry = int(input('1 >>> Change name\n2 >>> Change main photo\n3 >>> Messages\n>>> '))
            if entry == 1:
                name = input('Set name >>> ')
                await app.update_profile(first_name=name)
                print(me.first_name)
            elif entry == 2:
                entry = int(input('1 >>> Update \n2 >>> Remove\n>>> '))
                if entry == 1:
                    path = input('Path to photo >>> ').strip("'")
                    await app.set_profile_photo(photo=path)
                elif entry == 2:
                    photos = [p async for p in app.get_chat_photos("me")]
                    await app.delete_profile_photos(photos[0].file_id)
            elif entry == 3:
                entry = int(input('1 >>> Get login code\n2 >>> Get messages\n>>> '))
                my_ids = [d.chat.id async for d in app.get_dialogs()]  
                for id, i in enumerate(my_ids):
                    if i == 777000 and entry == 1:
                        async for message in app.get_chat_history(i, 1):
                            print(re.search(r'^.+[.]', message.text).group(0)[:-1]) 
                            exit()
                    elif entry == 2:
                        async for message in app.get_chat_history(i, 1):
                            if message.chat.first_name:
                                print('*** '+message.chat.first_name+' ***',  message.text, '\n', sep='\n')            
asyncio.run(main())

