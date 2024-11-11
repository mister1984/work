import asyncio
from pyrogram.raw import functions
from pyrogram.raw.types import InputPeerSelf, InputUser, InputReportReasonSpam, InputPeerUser, InputGeoPoint, ReactionEmoji, InputPeerChannel
from pyrogram import Client, enums 
from pyrogram.errors import *
import datetime
import pandas as pd
import random as r
import re
async def main():        
    t = r.randint(10, 30)
    n = int(input('Select number of bot >>> '))
    df = pd.DataFrame()
    df0 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='channels')
    df1 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='credentials')
    df2 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='join')
    df3 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='search')
    df4 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='published_posts')
    df5 = pd.read_excel('code/tg/bots_tg.xlsx', sheet_name='users')
    ids, links, titles, members, types, topics, dates, descriptions, repeated, bots, users, views  = [], [], [], [], [], [], [], [], [], [], [], []
    def adding():
        if chat.id < 0:
            if int(chat.members_count) > 1 and chat.id not in [j for j in df0['id']]:
                ids.append(chat.id)
                titles.append(chat.title)
                members.append(chat.members_count)
                descriptions.append(chat.description)
                try: links.append('https://t.me/'+chat.username)
                except: links.append('unknown')
                types.append(str(chat.type)[9:])
                topics.append(df2['topic'][id])
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
            df['topic'] = topics
            df.to_excel(f"{str(df1['who'][n])}-channels.xlsx")
        elif mode == 'statistic':
            df['link'] = links
            df['views'] = views
            df['members'] = members
            df.to_excel('TG_statistic.xlsx')
    def sub():
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
        i = re.sub('[«]', ' ', i)
        i = re.sub('[»]', ' ', i)
        i = re.sub('\n', ' ', i)
        i = re.sub(' +', ' ', i)
    try:
        groups_id = df1['groups_id'][n].split('-')
        next_id, last_id = int(groups_id[0])-2, int(groups_id[1])-2
    except AttributeError: 
        groups_id, min_id, max_id = -1, -1, -1
    message = df1['text'][n]
    try: media_id = df1['media_id'][n].split('$')
    except AttributeError: media_id = []
    async with Client(df1['app'][n], df1['id'][n], df1['hash'][n]) as app: 
        me = await app.get_me()
        my_first_name = me.first_name
        my_id = me.id
        entry = int(input(f'Welcome, {my_first_name}\n1 >>> groups\n2 >>> posts\n3 >>> users\n4 >>> settings\n5 >>> upload media\n6 >>> search post\n7 >>> get login code\n>>> '))
        if entry == 1:
            entry = int(input('0 >>> to_excel\n1 >>> join\n3 >>> search\n>>> '))
            if entry == 0:
                entry = int(input('1 >>> Get new\n2 >>> Get from dialogs\n>>> '))
                if entry == 1:
                    base_usernames = [i[13:].strip() for i in df2['link']]
                    my_base_usernames = [' '+i[13:].strip()+' ' for i in df0['link']]
                    for id, k in enumerate(base_usernames):
                        if last_id >= id >= next_id and ' '+k+' ' not in my_base_usernames:
                            try:
                                print(id)
                                chat = await app.get_chat(k)
                                await asyncio.sleep(0.25)
                                adding() 
                            except (AttributeError, TypeError) as e: print(e)
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
                my_diologs_usernames = [d.chat.username async for d in app.get_dialogs()]
                for id, i in enumerate(df0['link']):
                    i = str(i[13:].strip())
                    if last_id >= id >= next_id and i not in my_diologs_usernames:
                        try:
                            await app.join_chat(i)
                            print(id+2)
                            await asyncio.sleep(t)
                        except FloodWait as e:
                                print('Wait for', e.value, 'sec...')
                                if e.value > 7200: break
                                await asyncio.sleep(e.value)
                                await app.join_chat(i)
                                await asyncio.sleep(t)
                                print(id+2)
                        except (BadRequest, NotAcceptable, UserDeactivated) as e: print(e.MESSAGE)
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
            entry= int(input('1 >>> Send to chats\n2 >>> Send to user\n3 >>> Comment on post\n4 >>> Suggest post\n5 >>> Statistic on posts\n>>> '))
            if entry == 5:
                for id, i in enumerate(df4['link']):
                    if not isinstance(i, float):
                        i000 = i.strip()
                        i00 = i000.split('https://t.me/')
                        i1 = i00[1]
                        i0 = i1.split('/')
                        i1 = i0[0]
                        i2 = int(i0[1])
                        chat_members = await app.get_chat_members_count(i1)
                        post = await app.get_messages(i1, i2)
                        await asyncio.sleep(5)
                        links.append(i000)
                        views.append(post.views)
                        members.append(chat_members)
                        print(id)
                xlsx('statistic')
            else:
                for id, i in enumerate(df0['link']):
                    if last_id >= id >= next_id:
                        try:
                            if entry == 1 or entry == 2:
                                if len(media_id) == 0: await app.send_message(i, message)
                                elif len(media_id) > 0: await app.send_media_group(i, [InputMediaPhoto(media_id[0], caption=message)])  
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
            entry = int(input('1 >>> Get bot id\n2 >>> Join\n3 >>> Repost\n4 >>> Like\n5 >>> xxxx\n6 >>> YouScan parsing\n7 >>> Report peer\n8 >>> View\n>>> '))
            range_bots = input('Range bots >>> ').split('-')
            bot_next = int(range_bots[0])
            bot_last = int(range_bots[1])
            if entry == 7:
                user = input('User for report >>> ')
            elif entry == 2:
                link = input('Link on channel >>> ').split('https://t.me/')
                chat = link[1]
            elif entry == 4 or entry == 7 or entry == 8:
                chats, message_id = [], []
                for j in input('Link on posts >>> ').split(' '):
                    j = j.split('https://t.me/')
                    link = j[1].split('/')
                    chats.append(link[0])
                    message_id.append(int(link[1]))
                if entry == 4:
                    emojies = []
                    for j in input('Emojies >>> ').split(' '):
                        emojies.append(j)
            for id, i in enumerate(df1['app']):
                if bot_last >= id >= bot_next:
                    print(id)
                    try:
                        async with Client(i, df1['id'][n], df1['hash'][n]) as app:
                            if entry == 1: 
                                me = await app.get_me()
                                ids.append(me.id)
                            elif entry == 2: await app.join_chat(chat)
                            elif entry == 7 or entry == 8:
                                if entry == 7:
                                    peer = await app.resolve_peer(user)
                                    message = await app.get_messages(chat, message_id)
                                    await app.invoke(functions.account.ReportPeer(peer=peer, reason=InputReportReasonSpam(), message=message.caption)) 
                                elif entry == 8:
                                    peer = await app.resolve_peer(chat)
                                    await app.invoke(functions.messages.GetMessagesViews(peer=peer, id=[message_id], increment=True)) 
                            elif entry == 4:
                                for id1, chat in enumerate(chats):
                                    peer = await app.resolve_peer(chat)
                                    await app.invoke(functions.messages.GetMessagesViews(peer=peer, id=[message_id[id1]], increment=True))
                                    await app.invoke(functions.messages.SendReaction(peer=peer, msg_id=message_id[id1], reaction=[ReactionEmoji(emoticon=emojies[id1])]))
                    except (PeerIdInvalid, Unauthorized) as e: print(id, e.MESSAGE)
            if entry == 1: print(*ids, sep='\n')
            if entry == 6:
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
            entry = int(input('1 >>> Change name\n2 >>> Change main photo\n3 >>> Get last messages\n>>> '))
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
                my_ids = [d.chat.id async for d in app.get_dialogs()]  
                for id, i in enumerate(my_ids): 
                    async for message in app.get_chat_history(i, 1):
                        if message.chat.first_name: 
                            print('*** '+message.chat.first_name+' ***',  message.text, '\n', sep='\n')
        elif entry == 5:
            n_media = input('Path to media >>> ').split('  ')
            media = []
            for i in n_media:
                if re.search(r'[.]mp4', i.lower()):
                    video = await app.send_video(me.id, i)
                    media.append(video.video.file_id)
                else:
                    photo = await app.send_photo(me.id, i)
                    media.append(photo.photo.file_id)
            print(*media, sep='$')
        elif entry == 6:
            m0 = int(input('Min date (yyyymmdd) >>> '))
            link_used = [j.strip() for j in df4['link_used']]
            for q in df3['word'][0].split('$'):
                print(q, await app.search_global_count(q))
                async for message in app.search_global(q):
                    try: 
                        m1 = str(message.date)[:10]
                        m1 = int(re.sub('-', '', m1))
                    except (ValueError, AttributeError):
                        m1 = m0
                    if m1 >= m0:
                        if message.text:
                            i0 = message.text
                            i = message.text.lower()
                        elif message.caption:
                            i0 = message.caption
                            i = message.caption.lower()
                        if 'https' not in q: sub()
                        if ' '+q.lower()+' ' in ' '+i.lower().strip()+' ': 
                            try:
                                link = r'https://t.me/'+message.chat.username+r'/'+str(message.id)
                                if link not in links and link not in link_used:
                                    dates.append(message.date)
                                    links.append(link)
                                    titles.append(message.chat.title)
                                    descriptions.append(i0)
                            except TypeError:
                                dates.append(message.date)
                                link = r'-'
                                links.append(link)
                                titles.append(message.chat.title)
                                descriptions.append(i0)
            df['date'] = dates
            df['link'] = links
            df['title'] = titles
            df['description'] = descriptions
            if 'https' in str(df3['word'][0].split('$')[0]):df.to_excel('posts/'+'link'+str(me.id)+'.xlsx')
            else: df.to_excel('posts/'+str(df3['word'][0].split('$')[0])+str(me.id)+'.xlsx')
        elif entry == 7:
            async for message in app.get_chat_history(777000, 1):
                print(re.search(r'^.+[.]', message.text).group(0)[:-1]) 
asyncio.run(main())
